
from stages.stage5_filtering import stage5_selection_filtering

def test_filtering():
    # Mock documents
    docs = [
        {"title": "Paper 1", "url": "url1", "analysis": {}, "scoring": {"score": 8, "strengths": "s1", "weaknesses": "w1"}},
        {"title": "Paper 2", "url": "url2", "analysis": {}, "scoring": {"score": 9, "strengths": "s2", "weaknesses": "w2"}},
        {"title": "Paper 1", "url": "url3", "analysis": {}, "scoring": {"score": 7, "strengths": "s3", "weaknesses": "w3"}}, # Duplicate of 1, lower score
        {"title": "Paper 4", "url": "url4", "analysis": {}, "scoring": {"score": 6, "strengths": "s4", "weaknesses": "w4"}}, # Below threshold
        {"title": "Paper 5", "url": "url5", "analysis": {}, "scoring": {"score": 10, "strengths": "s5", "weaknesses": "w5"}},
    ]

    # Add more papers to test limiting
    for i in range(6, 16):
        docs.append({"title": f"Paper {i}", "url": f"url{i}", "analysis": {}, "scoring": {"score": 8, "strengths": f"s{i}", "weaknesses": f"w{i}"}})

    print(f"Total input docs: {len(docs)}")
    kb = stage5_selection_filtering(docs)

    print(f"Final KB size: {len(kb)}")

    # Assertions
    assert len(kb) <= 10
    assert kb[0]['source_title'] == "Paper 5" # Highest score should be first
    assert kb[1]['source_title'] == "Paper 2" # Second highest

    # Check deduplication (Paper 1 has score 8 and 7)
    paper1_entries = [d for d in kb if d['source_title'] == "Paper 1"]
    assert len(paper1_entries) == 1
    assert paper1_entries[0]['strengths'] == "s1" # Should be the one with score 8

    # Check threshold
    paper4_entries = [d for d in kb if d['source_title'] == "Paper 4"]
    assert len(paper4_entries) == 0

    print("Verification script passed successfully!")

if __name__ == "__main__":
    test_filtering()
