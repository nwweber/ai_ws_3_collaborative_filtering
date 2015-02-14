__author__ = 'niklas'

import unittest
import collaborative_filtering as cf
import pandas as pd
import math


class UserDistanceTest(unittest.TestCase):
    def test_calc_distances(self):
        u1_ratings = [1, 2, 3]
        u2_ratings = [1, 2, 3]
        u3_ratings = [2, 3, 4]
        ratings_dict = {0: u1_ratings,
                        1: u2_ratings,
                        2: u3_ratings}
        ratings_frame = pd.DataFrame(ratings_dict)
        dists = cf.calc_distances(ratings_frame, 0)
        expected = pd.Series([0, 0, math.sqrt(3)])
        self.assertTrue(expected.equals(dists))

# class AccuracyTest(unittest.TestCase):
# def testAccuray(self):
#         """"accuracy is calculated correctly"""
#         predicted = pd.Series([0, 0, 1, 1, 1])
#         real = pd.Series([0, 1, 0, 1, 1])
#         self.assertEqual(nb.calc_accuracy(predicted, real), 3 / 5)



if __name__ == "__main__":
    unittest.main()

