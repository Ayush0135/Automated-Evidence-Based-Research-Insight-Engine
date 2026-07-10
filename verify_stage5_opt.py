from stages.stage5_filtering import stage5_selection_filtering
import time

def test_stage5_optimization():
    print("Testing Stage 5 Optimization...")

    # Mock documents
    mock_docs = [
        {"title": "Paper A", "url": "url1", "analysis": {}, "scoring": {"score": 8, "strengths": "S1", "weaknesses": "W1"}},
        {"title": "Paper B", "url": "url2", "analysis": {}, "scoring": {"score": 6, "strengths": "S2", "weaknesses": "W2"}}, # Should be discarded
        {"title": "Paper A", "url": "url3", "analysis": {}, "scoring": {"score": 9, "strengths": "S3", "weaknesses": "W3"}}, # Duplicate of A, higher score
        {"title": "Paper C", "url": "url4", "analysis": {}, "scoring": {"score": 7, "strengths": "S4", "weaknesses": "W4"}},
        {"title": "Paper D", "url": "url5", "analysis": {}, "scoring": {"score": 10, "strengths": "S5", "weaknesses": "W5"}},
    ]

    # Add 10 more papers to test limiting
    for i in range(6, 20):
        mock_docs.append({
            "title": f"Paper {i}",
            "url": f"url{i}",
            "analysis": {},
            "scoring": {"score": 7.5, "strengths": f"S{i}", "weaknesses": f"W{i}"}
        })

    start_time = time.time()
    kb = stage5_selection_filtering(mock_docs)
    end_time = time.time()

    print(f"Filtering took {end_time - start_time:.6f} seconds.")

    # Assertions
    # 1. Discarded Paper B (score 6)
    titles = [doc['source_title'] for doc in kb]
    assert "Paper B" not in titles, "Paper B should have been discarded (score < 7)"

    # 2. Kept the best version of Paper A (score 9)
    paper_a_entries = [doc for doc in kb if doc['source_title'] == "Paper A"]
    assert len(paper_a_entries) == 1, "Should only have one unique entry for Paper A"
    assert paper_a_entries[0]['score'] == 9, "Should have kept the highest scoring version of Paper A"

    # 3. Sorted by score
    scores = [doc['score'] for doc in kb]
    assert scores == sorted(scores, reverse=True), "Knowledge base should be sorted by score descending"

    # 4. Limited to top 10
    assert len(kb) == 10, f"Expected 10 documents, got {len(kb)}"

    print("Verification SUCCESS: Sorting, Deduplication (Best-of), and Limiting are working correctly.")

if __name__ == "__main__":
    try:
        test_stage5_optimization()
    except AssertionError as e:
        print(f"Verification FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
