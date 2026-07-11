def stage5_selection_filtering(scored_documents):
    """
    Optimized selection and filtering:
    1. Sorts by score descending to prioritize quality.
    2. Limits to top 10 unique documents to minimize downstream LLM context/latency.
    3. Exits early when score falls below 7.0 or limit is reached.
    """
    print("\n--- STAGE 5: SELECTION & FILTERING ---")
    
    # Sort by score descending upfront so we can exit early
    scored_documents.sort(key=lambda x: x.get('scoring', {}).get('score', 0), reverse=True)

    knowledge_base = []
    seen_titles = set()
    
    for doc in scored_documents:
        # Stop if we have enough high-quality documents
        if len(knowledge_base) >= 10:
            break

        score = doc.get('scoring', {}).get('score', 0)
        
        # Stop early if the score falls below the threshold (since list is sorted)
        if score < 7:
            break
            
        title = doc.get('title', '')
        clean_title = title.lower().strip()

        if clean_title in seen_titles:
            # print(f"Discarding duplicate: {clean_title[:30]}")
            continue
            
        seen_titles.add(clean_title)
        
        # Build knowledge base entry in-place
        knowledge_base.append({
            "source_title": title,
            "url": doc.get('url'),
            "analysis": doc.get('analysis'),
            "strengths": doc.get('scoring', {}).get('strengths'),
            "weaknesses": doc.get('scoring', {}).get('weaknesses')
        })
        
    print(f"Retained {len(knowledge_base)} high-quality documents for synthesis.")
    return knowledge_base
