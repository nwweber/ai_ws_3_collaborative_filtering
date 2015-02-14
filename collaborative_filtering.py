__author__ = 'niklas'

import pandas as pd
import math


def calc_distances_euclidean(ratings_frame, uid):
    """
    calculate euclidean distances from this user
    :param ratings_frame: pd.Frame, index = itemId, columns = users
    :param uid:
    :return: pd.Series, index = user id, value = distance
    """
    user = ratings_frame[uid]
    dists_dict = {column: math.sqrt(((series - user)**2).sum()) for column, series in ratings_frame.iteritems()}
    return pd.Series(dists_dict)


# find the k closest users to a given user u

def find_k_closest_users(ratings_frame, uid, k):
    distance_series = calc_distances_euclidean(ratings_frame, uid)
    distance_series = distance_series.order(ascending=False)
    del distance_series[uid]
    assert len(distance_series) >= k
    return list(distance_series.index[0:(k + 1)])


if __name__ == "__main__":
    pass