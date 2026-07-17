from utils.search import google_search, download_and_parse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_search_item(item):
    """
    Helper function to process a single search result:
    - Downloads and parses content
    """
    url = item.get('link')
    title = item.get('title')
    snippet = item.get('snippet')

    try:
        raw_text = download_and_parse(url)
        if len(raw_text) < 500: # Too short to be a paper
            return None
        
        return {
            "title": title,
            "url": url,
            "snippet": snippet,
            "raw_text": raw_text
        }
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def stage2_document_discovery(decomposition_data, existing_urls=None, existing_titles=None):
    """
    Finds academic papers and documents based on the decomposition subtopics and queries.
    Supports cross-stage deduplication by passing already-processed existing_urls and existing_titles.
    """
    print("\n--- STAGE 2: DOCUMENT DISCOVERY ---")
    
    all_documents = []
    # Initialize seen sets with existing documents from previous stages to prevent duplicate downloads and processing
    seen_urls = set(existing_urls) if existing_urls else set()
    seen_titles = set(existing_titles) if existing_titles else set()
    search_candidates = []
    skip_domains = ['youtube.com', 'news.google.com', 'wikipedia.org']
    
    if not decomposition_data or 'subtopics' not in decomposition_data:
        print("Invalid input for Stage 2")
        return []

    # 1. Gather all candidates concurrently
    def execute_search_query(subtopic, query, keywords):
        results = []
        # Enforce academic constraints in query
        academic_query = f"{query} filetype:pdf OR site:.edu OR site:.org \"research paper\""
        print(f"  [Search] Querying: {academic_query}")
        
        try:
            # Removed redundant sleep to speed up parallel search
            search_res = google_search(academic_query, num_results=6) # Reduced from 8 to 6 for speed
            for item in search_res:
                item['subtopic'] = subtopic['name']
                item['keywords'] = keywords
                results.append(item)
        except Exception as e:
            print(f"    Error querying Google for '{query}': {e}")
        return results

    # Flatten all queries and pre-calculate keywords
    all_queries = []
    subtopic_keywords_cache = {}
    for subtopic in decomposition_data['subtopics']:
        name = subtopic['name']
        if name not in subtopic_keywords_cache:
            # keywords > 3 chars to avoid 'the', 'and', 'for'
            subtopic_keywords_cache[name] = [k.lower() for k in name.split() if len(k) > 3]

        keywords = subtopic_keywords_cache[name]
        for query in subtopic['search_queries']:
            all_queries.append((subtopic, query, keywords))

    print(f"Executing {len(all_queries)} search queries in parallel...")
    
    with ThreadPoolExecutor(max_workers=5) as search_executor:
        future_to_query = {search_executor.submit(execute_search_query, s, q, k): (s, q, k) for s, q, k in all_queries}
        
        for future in as_completed(future_to_query):
            results = future.result()
            for item in results:
                url = item.get('link')
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                keywords = item.get('keywords', [])

                if url in seen_urls:
                    continue

                # Title-based deduplication
                clean_title = title.lower().strip()
                if clean_title in seen_titles:
                    continue

                # 1. Domain Filtering (Upfront)
                if any(x in url for x in skip_domains):
                    continue

                # 2. Relevance Filtering (Upfront)
                if keywords:
                    text_to_check = (title + " " + snippet).lower()
                    if not any(k in text_to_check for k in keywords):
                        continue

                seen_urls.add(url)
                seen_titles.add(clean_title)
                # print(f"    Found: {item.get('title')[:40]}...")
                search_candidates.append(item)

    # Limit to top 20 candidates total (User Constraint)
    if len(search_candidates) > 20:
        print(f"Limiting candidates from {len(search_candidates)} to top 20.")
        search_candidates = search_candidates[:20]

    print(f"\nDownloading and parsing {len(search_candidates)} candidates in parallel...")

    # 2. Process downloads in parallel
    # Increased max_workers to 10 to better utilize connection pooling (up to 20)
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_item = {executor.submit(process_search_item, item): item for item in search_candidates}
        
        for future in as_completed(future_to_item):
            result = future.result()
            if result:
                all_documents.append(result)
                print(f"    + Downloaded: {result['title'][:40]}...")
            else:
                # Optional: indicate skip/failure
                pass
    
    print(f"Total documents retrieved: {len(all_documents)}")
    return all_documents
