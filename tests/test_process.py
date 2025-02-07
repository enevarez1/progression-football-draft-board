import unittest

from src.report.model import Evaluation, Player
from src.report.process import convert_float_to_feet, convert_string_to_float, most_likely_raw_overall

class TestProcess(unittest.TestCase):
    def testMostLikelyOverall2Range(self):
        evaluations = Evaluation(74, 2, 65)
        player = Player("first", "last", "QB", 21, 10001, "strategic", evaluations)
        player.evaluation.append(Evaluation(70, 2, 65)),
        player.evaluation.append(Evaluation(72, 2, 65)),
        player.evaluation.append(Evaluation(83, 5, 50))
        most_likely, weight_likely = most_likely_raw_overall(player)
        self.assertEqual(most_likely, 73.25)
        self.assertEqual(weight_likely, 70.11)

    
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
