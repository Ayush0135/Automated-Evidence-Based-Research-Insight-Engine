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
    snippet = item.get('snippet', '')
    
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

def stage2_document_discovery(decomposition_data):
    print("\n--- STAGE 2: DOCUMENT DISCOVERY ---")
    
    all_documents = []
    seen_urls = set()
    search_candidates = []
    
    if not decomposition_data or 'subtopics' not in decomposition_data:
        print("Invalid input for Stage 2")
        return []

    # 1. Gather all candidates concurrently
    # Pre-calculate keywords for each subtopic to avoid redundant computation
    for subtopic in decomposition_data['subtopics']:
        subtopic['keywords_list'] = [k.lower() for k in subtopic['name'].split() if len(k) > 3]

    def execute_search_query(subtopic, query):
        results = []
        # Enforce academic constraints in query
        academic_query = f"{query} filetype:pdf OR site:.edu OR site:.org \"research paper\""
        print(f"  [Search] Querying: {academic_query}")
        
        try:
            # Removed redundant sleep to speed up parallel search
            search_res = google_search(academic_query, num_results=6) # Reduced from 8 to 6 for speed
            for item in search_res:
                item['keywords_list'] = subtopic['keywords_list']
                results.append(item)
        except Exception as e:
            print(f"    Error querying Google for '{query}': {e}")
        return results

    # Flatten all queries
    all_queries = []
    for subtopic in decomposition_data['subtopics']:
        for query in subtopic['search_queries']:
            all_queries.append((subtopic, query))

    print(f"Executing {len(all_queries)} search queries in parallel...")
    
    # Filter trivial non-academic URLs (heuristic)
    skip_domains = ['youtube.com', 'news.google.com', 'wikipedia.org']

    with ThreadPoolExecutor(max_workers=5) as search_executor:
        future_to_query = {search_executor.submit(execute_search_query, s, q): (s, q) for s, q in all_queries}
        
        for future in as_completed(future_to_query):
            results = future.result()
            for item in results:
                url = item.get('link')
                if not url or url in seen_urls:
                    continue

                # OPTIMIZATION: Filter domains UPFRONT before truncation
                if any(x in url for x in skip_domains):
                    continue

                # OPTIMIZATION: Relevance check UPFRONT before truncation
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                keywords = item.get('keywords_list', [])
                if keywords:
                    text_to_check = (title + " " + snippet).lower()
                    if not any(k in text_to_check for k in keywords):
                        continue

                seen_urls.add(url)
                search_candidates.append(item)

    # Limit to top 20 candidates total (User Constraint)
    if len(search_candidates) > 20:
        print(f"Limiting candidates from {len(search_candidates)} to top 20.")
        search_candidates = search_candidates[:20]

    print(f"\nDownloading and parsing {len(search_candidates)} candidates in parallel...")

    # 2. Process downloads in parallel
    # max_workers=5 is a safe number to not overwhelm network or get IP blocked
    with ThreadPoolExecutor(max_workers=5) as executor:
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
