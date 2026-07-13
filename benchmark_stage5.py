import time
import copy

# Mocking the original logic for comparison
def original_stage5(scored_documents):
    high_quality_docs = []
    seen_titles = set()
    for doc in scored_documents:
        score = doc.get('scoring', {}).get('score', 0)
        title = doc.get('title', '').lower()
        if score < 7:
            continue
        if title in seen_titles:
            continue
        seen_titles.add(title)
        high_quality_docs.append(doc)
    knowledge_base = []
    for doc in high_quality_docs:
        entry = {
            "source_title": doc['title'],
            "url": doc['url'],
            "analysis": doc['analysis'],
            "strengths": doc['scoring'].get('strengths'),
            "weaknesses": doc['scoring'].get('weaknesses')
        }
        knowledge_base.append(entry)
    return knowledge_base

from stages.stage5_filtering import stage5_selection_filtering as optimized_stage5

def benchmark():
    # 1000 dummy documents
    docs = []
    for i in range(1000):
        docs.append({
            "title": f"Paper {i}",
            "url": f"http://example.com/{i}",
            "analysis": {"data": "x" * 100},
            "scoring": {"score": (i % 10), "strengths": "S", "weaknesses": "W"}
        })

    # Benchmark original
    docs_orig = copy.deepcopy(docs)
    start = time.perf_counter()
    res_orig = original_stage5(docs_orig)
    end = time.perf_counter()
    orig_time = end - start
    print(f"Original Stage 5 Time: {orig_time:.6f}s (Retained: {len(res_orig)})")

    # Benchmark optimized
    docs_opt = copy.deepcopy(docs)
    start = time.perf_counter()
    res_opt = optimized_stage5(docs_opt)
    end = time.perf_counter()
    opt_time = end - start
    print(f"Optimized Stage 5 Time: {opt_time:.6f}s (Retained: {len(res_opt)})")

    if opt_time < orig_time:
        improvement = (orig_time - opt_time) / orig_time * 100
        print(f"Improvement: {improvement:.2f}%")
    else:
        print("No measurable improvement in this micro-benchmark.")

if __name__ == "__main__":
    benchmark()
