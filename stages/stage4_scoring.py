from utils.llm import query_groq, extract_json
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def score_single_document(doc, topic):
    """
    Helper function to score a single document using an LLM.
    """
    analysis = doc.get('analysis', {})
    if not analysis:
        return None

    # print(f"Scoring: {doc['title'][:50]}...")

    prompt = f"""
    Role: Strict Academic Reviewer.
    Target Research Topic: "{topic}"

    Document Title: {doc['title']}
    Analysis Summary:
    - Problem: {analysis.get('research_problem')}
    - Method: {analysis.get('methodology')}
    - Findings: {analysis.get('key_findings')}
    - Novelty: {analysis.get('novelty_assessment')}

    Evaluate based on:
    1. Novelty
    2. Methodological rigor
    3. Relevance to the research topic
    4. Academic clarity
    5. Suitability for Scopus-indexed journals

    Return ONLY valid JSON:
    {{
      "score": number (0-10),
      "strengths": "string",
      "weaknesses": "string"
    }}

    No explanations. No markdown.
    """

    try:
        response = query_groq(prompt, json_mode=True, fallback_to_others=True)
        score_data = extract_json(response)

        if not score_data:
            return None

        doc['scoring'] = score_data
        return doc
    except Exception as e:
        print(f"  Error scoring document {doc.get('title', 'Unknown')}: {e}")
        return None

def stage4_academic_scoring(analyzed_documents, topic):
    print("\n--- STAGE 4: ACADEMIC SCORING (Parallel) ---")
    scored_documents = []
    
    # Use ThreadPoolExecutor to parallelize scoring.
    # 3 workers is a balance between speed and avoiding rate limits.
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_doc = {executor.submit(score_single_document, doc, topic): doc for doc in analyzed_documents}
        
        for future in as_completed(future_to_doc):
            result = future.result()
            if result:
                scored_documents.append(result)
                print(f"  + Scored: {result['title'][:40]}... [Score: {result['scoring'].get('score')}]")
            
    return scored_documents
