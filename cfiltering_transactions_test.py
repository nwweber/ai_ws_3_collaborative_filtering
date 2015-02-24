__author__ = 'niklas'

__author__ = 'niklas'

import unittest
import cfiltering_transactions as cf
import pandas as pd
import math
import numpy as np


class UserDistanceTest(unittest.TestCase):
    def setUp(self):
        self.ratings = pd.DataFrame(data={"user": [0, 1]*2,
                                          "item": [10, 10, 11, 12],
                                          "rating": [1, 4, 2, 4]})

    def test_calc_distances(self):
        dists = cf.calc_distances_euclidean(self.ratings, 0)
        expected = pd.Series(data=[math.sqrt(3**2)], index=[1])
        self.assertTrue(expected.equals(dists))

    def test_find_k_closest_users(self):
        expecteds = [2, 1]
        for expected, result in zip(expecteds, cf.find_k_closest_users(self.ratings, 0, 2)):
            self.assertEqual(expected, result)

    def test_calc_item_distance_cosine(self):
        raise NotImplementedError

# class AccuracyTest(unittest.TestCase):
# def testAccuray(self):
# """"accuracy is calculated correctly"""
# predicted = pd.Series([0, 0, 1, 1, 1])
# real = pd.Series([0, 1, 0, 1, 1])
#         self.assertEqual(nb.calc_accuracy(predicted, real), 3 / 5)



if __name__ == "__main__":
    unittest.main()

