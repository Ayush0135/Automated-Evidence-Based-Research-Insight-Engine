from utils.llm import query_groq
import json
import re
from concurrent.futures import ThreadPoolExecutor

def score_single_document(doc, topic):
    """
    Helper function to score a single document using the LLM.
    Refactored for parallel execution in Stage 4.
    """
    analysis = doc.get('analysis', {})
    if not analysis:
        return None

    print(f"Scoring: {doc['title'][:50]}...")

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
        print(f"  Score: {score_data.get('score')} - {doc['title'][:30]}...")
        return doc
    except Exception as e:
        print(f"  Error scoring document {doc['title'][:20]}: {e}")
        return None

def stage4_academic_scoring(analyzed_documents, topic):
    """
    Stage 4: Academic Scoring.
    Parallelized with 3 workers to achieve ~3x speedup while maintaining document order.
    """
    print("\n--- STAGE 4: ACADEMIC SCORING (Parallel) ---")
    scored_documents = []
    
    # max_workers=3 balance between speed and rate limits
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all documents for scoring
        futures = [executor.submit(score_single_document, doc, topic) for doc in analyzed_documents]
        
        # Gather results by iterating over futures in SUBMISSION ORDER to preserve relevance-based ranking
        for future in futures:
            result = future.result()
            if result:
                scored_documents.append(result)
            
    return scored_documents
