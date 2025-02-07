import unittest

from src.report.process import convert_float_to_feet, convert_string_to_float, most_likely_raw_overall

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

    def testConvertStringToFloat(self):
        answer = convert_string_to_float("10'5\"")
        self.assertEqual(125, answer)

    def testConvertFloatToString(self):
        answer = convert_float_to_feet(125)
        self.assertEqual("10'5\"", answer)

if __name__ == '__main__':
    unittest.main()
