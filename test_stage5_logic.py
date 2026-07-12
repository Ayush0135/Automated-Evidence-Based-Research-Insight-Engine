import unittest
from stages.stage5_filtering import stage5_selection_filtering

class TestStage5Logic(unittest.TestCase):
    def test_sorting_and_filtering(self):
        # Create dummy documents with varied scores
        docs = [
            {"title": "P1", "url": "u1", "analysis": {}, "scoring": {"score": 2}},
            {"title": "P2", "url": "u2", "analysis": {}, "scoring": {"score": 9}},
            {"title": "P3", "url": "u3", "analysis": {}, "scoring": {"score": 7}},
            {"title": "P4", "url": "u4", "analysis": {}, "scoring": {"score": 10}},
            {"title": "P5", "url": "u5", "analysis": {}, "scoring": {"score": 5}},
        ]

        kb = stage5_selection_filtering(docs)

        # Should retain P4 (10), P2 (9), P3 (7)
        self.assertEqual(len(kb), 3)
        self.assertEqual(kb[0]['source_title'], "P4")
        self.assertEqual(kb[1]['source_title'], "P2")
        self.assertEqual(kb[2]['source_title'], "P3")

    def test_limit_10(self):
        # 15 papers with score 9
        docs = []
        for i in range(1, 16):
            docs.append({
                "title": f"High Quality {i}",
                "url": f"http://example.com/{i}",
                "analysis": {},
                "scoring": {"score": 9, "strengths": "S", "weaknesses": "W"}
            })

        kb = stage5_selection_filtering(docs)
        self.assertEqual(len(kb), 10)

    def test_deduplication(self):
        docs = [
            {"title": "Dup", "url": "u1", "analysis": {}, "scoring": {"score": 9}},
            {"title": "dup", "url": "u2", "analysis": {}, "scoring": {"score": 8}},
            {"title": "Unique", "url": "u3", "analysis": {}, "scoring": {"score": 7}}
        ]
        kb = stage5_selection_filtering(docs)
        self.assertEqual(len(kb), 2)
        self.assertEqual(kb[0]['source_title'], "Dup")
        self.assertEqual(kb[1]['source_title'], "Unique")

if __name__ == "__main__":
    unittest.main()
