def stage5_selection_filtering(scored_documents):
    print("\n--- STAGE 5: SELECTION & FILTERING ---")
    
    # 1. Sort by score descending upfront to ensure we keep the highest-quality version during deduplication
    # This also ensures the final knowledge base is prioritized by academic quality.
    scored_documents.sort(key=lambda x: x.get('scoring', {}).get('score', 0), reverse=True)

    high_quality_docs = []
    seen_titles = set()
    
    for doc in scored_documents:
        # Optimization: Early exit if we reached the desired capacity
        # Reducing the knowledge base size improves downstream LLM latency in Stages 6 & 7.
        if len(high_quality_docs) >= 10:
            break

        score = doc.get('scoring', {}).get('score', 0)
        
        # Quality Threshold: 7.0/10
        # Since we sorted, once we hit score < 7, all subsequent docs are also < 7.
        if score < 7:
            break
            
        title = doc.get('title', '').lower().strip()
        if title in seen_titles:
            # We already have a higher-scoring (or equal) version of this paper
            continue
            
        seen_titles.add(title)
        high_quality_docs.append(doc)

    print(f"Retained {len(high_quality_docs)} unique high-quality documents.")
    
    # Compile the analysis fields into a structured knowledge base
    knowledge_base = []
    for doc in high_quality_docs:
        entry = {
            "source_title": doc['title'],
            "url": doc['url'],
            "analysis": doc['analysis'],
            "strengths": doc['scoring'].get('strengths'),
            "weaknesses": doc['scoring'].get('weaknesses'),
            "score": doc['scoring'].get('score')
        }
        knowledge_base.append(entry)
        
    return knowledge_base
