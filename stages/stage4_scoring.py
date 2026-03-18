from utils.llm import query_groq
import json
import re
from concurrent.futures import ThreadPoolExecutor

def score_single_document(doc, topic):
    """
    Helper function to score a single document using an LLM.
    Preserves document structure and adds scoring information.
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
        print(f"  + Scored: {doc['title'][:30]}... (Score: {score_data.get('score')})")
        return doc
    except Exception as e:
        print(f"  x Error scoring document {doc['title'][:20]}: {e}")
        return None

def stage4_academic_scoring(analyzed_documents, topic):
    """
    Parallelized Stage 4: Scores documents for academic quality and relevance.
    Uses ThreadPoolExecutor for concurrent LLM calls while preserving document order.
    """
    print("\n--- STAGE 4: ACADEMIC SCORING (Parallel) ---")
    scored_documents = []
    
    # Using max_workers=3 for parallel throughput while minimizing rate limits
    # Performance Impact: ~3x speedup for Stage 4 execution.
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks and keep track of futures to preserve original order
        futures = [executor.submit(score_single_document, doc, topic) for doc in analyzed_documents]
        
        # Iterating directly over futures list ensures results are collected in submission order
        for future in futures:
            try:
                result = future.result()
                if result:
                    scored_documents.append(result)
            except Exception as e:
                print(f"  ! Future error: {e}")
                
    return scored_documents
