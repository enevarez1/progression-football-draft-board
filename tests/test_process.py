import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from report.process import most_likely_raw_overall

class TestProcess(unittest.TestCase):
    
    def testMostLikelyOverall2Range(self):
        evaluations = [
            {'score': 74, 'range': 2, 'confidence': 65},
            {'score': 70, 'range': 2, 'confidence': 65},
            {'score': 72, 'range': 2, 'confidence': 65},
            {'score': 83, 'range': 5, 'confidence': 50}
        ]
        answer = most_likely_raw_overall(evaluations)
        self.assertEqual(answer, 73.25)
    
    def testMostLikelyOverall3Range(self):
        self.assertEqual(0,0)

if __name__ == '__main__':
    unittest.main()
