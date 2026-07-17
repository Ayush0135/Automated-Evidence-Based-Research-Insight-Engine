from utils.llm import query_gemini, extract_json
import json
import re
import time

def chunk_text(text, chunk_size=128000, overlap=2000):
    """
    Splits text into overlapping chunks.
    Optimized to use 128,000 character chunks to align with modern LLM high context limits.
    """
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end])
        # Move forward, but backtrack by overlap amount
        start += (chunk_size - overlap)
        
        # Avoid infinite loop if overlap >= chunk_size (shouldn't happen with these defaults)
        if start >= text_len:
            break
            
    return chunks

from concurrent.futures import ThreadPoolExecutor, as_completed

def analyze_single_document(doc):
    try:
        # print(f"Analyzing: {doc['title'][:30]}...")
        full_text = doc['raw_text']
        
        # Strategy Decision: Chunk vs Whole
        # Optimization: Increased threshold to 128,000 characters to handle academic papers in a single call,
        # reducing parallel chunk analysis overhead and API latency.
        if len(full_text) > 128000:
            # print(f"  - Large Doc ({len(full_text)} chars). Chunking...")
            all_chunks = chunk_text(full_text, chunk_size=128000, overlap=2000)
            
            # Smart Selection: Limit to max 6 chunks for speed
            if len(all_chunks) > 6:
                # First 2, Middle 2, Last 2
                mid = len(all_chunks) // 2
                selected_chunks = all_chunks[:2] + all_chunks[mid:mid+2] + all_chunks[-2:]
            else:
                selected_chunks = all_chunks
            
            chunk_summaries = []
            
            # Parallel Chunk Analysis (Mini-batch)
            def analyze_chunk(idx, chunk):
                chunk_prompt = f"""
                Analyze this segment (Part {idx+1}) of "{doc['title']}".
                Segment: {chunk}
                Task: Extract Research Problem, Methodology, Findings, Limitations.
                Output: Concise bullet points.
                """
                try:
                    return query_gemini(chunk_prompt, fallback_to_others=True)
                except:
                    return ""

            with ThreadPoolExecutor(max_workers=3) as chunk_executor:
                # Use executor.map to maintain logical order of chunk summaries
                indices = range(len(selected_chunks))
                results = list(chunk_executor.map(analyze_chunk, indices, selected_chunks))
                chunk_summaries = [res for res in results if res]
            
            text_context = "\n".join(chunk_summaries)
        else:
            # For documents under the threshold, use up to 128,000 characters
            text_content = full_text[:128000]
            text_context = text_content

        prompt = f"""
        Analyze the following research document content (or extracted summaries of it).
        
        Document Title: {doc['title']}
        
        Content/Context:
        {text_context}
        
        Task:
        1. Extract the research problem (Be specific).
        2. Identify methodology (Include specific model names, algorithms, parameter counts, equations if described).
        3. Summarize key findings (Include quantitative metrics like accuracy, F1-score, latency, user study statistics where available).
        4. Identify limitations and weaknesses.
        5. Detect explicit or implicit research gaps.
        6. Assess novelty.
        7. Evaluate detailedness: Does it provide implementation details?
        
        Constraint:
        - All output must be paraphrased. Do NOT copy text verbatim.
        - Focus on extracting *knowledge*, not just describing the paper.
        
        Output Format (JSON strictly):
        {{
            "research_problem": "string",
            "methodology": "string",
            "key_findings": "string",
            "limitations": "string",
            "research_gaps": "string",
            "novelty_assessment": "string",
            "technical_depth_score": 5, 
            "missing_entities": "string (list of missing specific details)"
        }}
        """
        
        response = query_gemini(prompt, fallback_to_others=False)
        
        # Robust Parsing using centralized helper
        analysis = extract_json(response)
        if not analysis:
            # Fallback: If model text isn't JSON, wrap it anyway so we don't lose the data
            print(f"  ! Warning: Could not parse JSON for {doc['title'][:15]}. Using raw text fallback.")
            analysis = {
                "research_problem": "JSON Parsing Failed",
                "methodology": "See findings",
                "key_findings": response if response else "No content returned",
                "limitations": "N/A",
                "research_gaps": "N/A",
                "novelty_assessment": "N/A",
                "technical_depth_score": 0,
                "missing_entities": "Parsing Failed"
            }
        
        doc['analysis'] = analysis
        print(f"  + Analysis Complete: {doc['title'][:30]}...")
        return doc
        
    except Exception as e:
        print(f"  x Error analyzing {doc['title'][:20]}: {e}")
        return None

def stage3_document_analysis(documents):
    print("\n--- STAGE 3: DOCUMENT ANALYSIS (Parallel) ---")
    analyzed_documents = []
    
    # Process documents in parallel
    # Increased max_workers to 4 for faster document throughput
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_doc = {executor.submit(analyze_single_document, doc): doc for doc in documents}
        
        for future in as_completed(future_to_doc):
            result = future.result()
            if result:
                analyzed_documents.append(result)
                
    return analyzed_documents
