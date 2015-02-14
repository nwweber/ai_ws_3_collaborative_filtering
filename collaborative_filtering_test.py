__author__ = 'niklas'

import unittest
import collaborative_filtering as cf
import pandas as pd
import math


class UserDistanceTest(unittest.TestCase):
    def setUp(self):
        self.u1_ratings = [1, 2, 3]
        self.u2_ratings = [1, 2, 3]
        self.u3_ratings = [2, 3, 4]
        self.ratings_dict = {0: self.u1_ratings,
                             1: self.u2_ratings,
                             2: self.u3_ratings}
        self.ratings_frame = pd.DataFrame(self.ratings_dict)

    def test_calc_distances(self):
        dists = cf.calc_distances_euclidean(self.ratings_frame, 0)
        expected = pd.Series([0, 0, math.sqrt(3)])
        self.assertTrue(expected.equals(dists))

    def test_find_k_closest_users(self):
        expecteds = [2, 1]
        for expected, result in zip(expecteds, cf.find_k_closest_users(self.ratings_frame, 0, 2)):
            self.assertEqual(expected, result)

# class AccuracyTest(unittest.TestCase):
# def testAccuray(self):
# """"accuracy is calculated correctly"""
#         predicted = pd.Series([0, 0, 1, 1, 1])
#         real = pd.Series([0, 1, 0, 1, 1])
#         self.assertEqual(nb.calc_accuracy(predicted, real), 3 / 5)



if __name__ == "__main__":
    unittest.main()

