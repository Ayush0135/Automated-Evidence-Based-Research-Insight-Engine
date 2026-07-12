def stage5_selection_filtering(scored_documents):
    """
    Filters and sorts scored documents to create a high-quality knowledge base.
    Optimized to sort by score, limit to 10 docs, and use a single pass for efficiency.
    """
    print("\n--- STAGE 5: SELECTION & FILTERING ---")
    
    # Optimization: Sort by score descending upfront to prioritize highest quality
    # and allow for early exit. Using sorted() to avoid side-effects on input and support iterables.
    sorted_docs = sorted(scored_documents, key=lambda x: x.get('scoring', {}).get('score', 0), reverse=True)

    knowledge_base = []
    seen_titles = set()
    
    for doc in sorted_docs:
        # Early exit if we already have 10 high-quality documents
        if len(knowledge_base) >= 10:
            break

        score = doc.get('scoring', {}).get('score', 0)
        title = doc.get('title', '').lower()
        
        # Early exit: Since we sorted, all subsequent documents will have score <= current
        if score < 7:
            break
            
        if title in seen_titles:
            continue
            
        seen_titles.add(title)
        
        # Optimization: Build the knowledge base entry in the same pass
        entry = {
            "source_title": doc['title'],
            "url": doc['url'],
            "analysis": doc['analysis'],
            "strengths": doc['scoring'].get('strengths'),
            "weaknesses": doc['scoring'].get('weaknesses')
        }
        knowledge_base.append(entry)
        
    print(f"Retained {len(knowledge_base)} high-quality documents.")
    return knowledge_base
