from utils.llm import query_groq
import json
import re
from concurrent.futures import ThreadPoolExecutor

def score_single_document(doc, topic):
    """
    Score a single document using Groq.
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
        # Robust Extraction
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            json_str = match.group(0)
            score_data = json.loads(json_str)
        else:
            # Fallback to direct load or primitive cleanup
            cleaned = response.replace("```json", "").replace("```", "").strip()
            score_data = json.loads(cleaned)

        doc['scoring'] = score_data
        return doc
    except Exception as e:
        print(f"  Error scoring document {doc.get('title', 'Unknown')[:30]}: {e}")
        return None

def stage4_academic_scoring(analyzed_documents, topic):
    print("\n--- STAGE 4: ACADEMIC SCORING (Groq Parallel) ---")
    scored_documents = []
    
    # Using 3 workers for Stage 4 to speed up scoring while preserving document order
    # Parallelizing reduces execution time by ~3x for large document sets.
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks and keep track of futures in order
        futures = [executor.submit(score_single_document, doc, topic) for doc in analyzed_documents]
        
        # Gather results in the same order they were submitted
        for i, future in enumerate(futures):
            doc = analyzed_documents[i]
            print(f"Scoring: {doc['title'][:50]}...")

            result = future.result()
            if result:
                scored_documents.append(result)
                print(f"  Score: {result['scoring'].get('score')}")
            
    return scored_documents
