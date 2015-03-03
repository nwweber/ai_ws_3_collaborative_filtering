import time
import multiprocessing

__author__ = 'niklas'

import os
import pandas as pd
import math
import numpy as np

def euclidean_distance(series_tuple):
    s1, s2 = series_tuple


def find_ratings(uid, ratings):
    ratings_series = ratings[ratings["user"] == uid][["item", "rating"]]
    ratings_series = ratings_series.set_index("item")
    return ratings_series


def _calc_distances_process(arg_dict):
    base_ratings = arg_dict["base_ratings"]
    ratings = arg_dict["ratings"]
    other_user = arg_dict["other_user"]
    q = arg_dict["q"]
    # get other user's ratings
    other_ratings = find_ratings(other_user, ratings)
    # reduce to common ratings
    common_ratings = pd.merge(base_ratings, other_ratings, left_index=True, right_index=True, how="inner")
    # calc distance to base user
    if len(common_ratings) > 0:
        dist = ((common_ratings["rating_x"] - common_ratings["rating_y"])**2).sum()
        # print("calculated the distance as", dist)
    else:
        dist = np.NAN
    q.put((other_user, dist))
    return None

def calc_distances_euclidean(ratings, base_uid):
    """
    Calculate Euclidean distances of other users to user indicated by base_uid
    Distance = Eucl. dist. between vectors of (shared) ratings
    :param ratings: ratings transactions frame
    :param base_uid: compare other users ot this
    :return: pd.Series, index = uid, data = distance to base_uid
    """
    print("base user: ", base_uid)
    # get list of users
    all_uids = ratings["user"].unique()
    # eliminate base user
    other_uids = all_uids[all_uids != base_uid]
    #############################
    # experimentation
    #############################
    other_uids = other_uids[:4000]
    # get base user ratings
    base_ratings = find_ratings(base_uid, ratings)
    # for each other user:
    dists = {}
    nr_other_users = len(other_uids)

    q = multiprocessing.SimpleQueue()
    pool = multiprocessing.Pool()
    # p = multiprocessing.Process(target=_calc_distances_process, args=(base_ratings, ratings, other_uids[0], q))
    # p.start()
    # p.join()
    # dist_tuples = []
    # while not q.empty():
    #     dist_tuples.append(q.get())
    pool_iterables = [{"base_ratings": base_ratings, "ratings": ratings, "q": q, "other_user": other_user} for other_user in other_uids]
    dist_tuples = pool.map(_calc_distances_process, pool_iterables)
    return pd.Series({uid: dist for (uid, dist) in dist_tuples})

    #
    # for i, other_user in enumerate(other_uids):
    #     if i % 1000 == 0:
    #         print("processing other user", other_user)
    #         print("this is user ", i, "out of", nr_other_users)
    #     # get other user's ratings
    #     other_ratings = find_ratings(other_user, ratings)
    #     # reduce to common ratings
    #     common_ratings = pd.merge(base_ratings, other_ratings, left_index=True, right_index=True, how="inner")
    #     # calc distance to base user
    #     if len(common_ratings) > 0:
    #         dist = ((common_ratings["rating_x"] - common_ratings["rating_y"])**2).sum()
    #         # print("calculated the distance as", dist)
    #     else:
    #         dist = np.NAN
    #     dists[other_user] = dist
    # # return user<->rating pairs/series
    # return pd.Series(dists)


def load_rating_data():
    data_path = os.path.join("data", "BX-CSV-Dump", "BX-Book-Ratings.csv")
    ratings = pd.read_csv(data_path, sep=";", encoding="latin1")
    ratings.columns = ["user", "item", "rating"]
    return ratings


def find_k_closest_users(ratings, user_id, k):
    # find distances to other users
    start = time.clock()
    distances = calc_distances_euclidean(ratings, user_id)
    end = time.clock()
    print("Time spent calculating distances:", end-start)
    # sort on distances, drop NANs
    distances.sort()
    distances = distances.dropna()
    # pick and return k closest
    return distances[:k]


def find_k_closest_items(ratings, param, param1):
    pass


def find_k_recommended_items(user, item, ratings):
    pass


def delete_some_ratings(ratings):
    pass


def predict_rating(user, item, ratings):
    pass


if __name__ == "__main__":
    # load data
    print("loading data")
    ratings = load_rating_data()
    print("done loading data")
    # find 10 closest users
    closest_users = find_k_closest_users(ratings, 170155, 10)
    print("closest users:", closest_users)
    # # find 10 closest items to 836218221
    # closest_items = find_k_closest_items(ratings, 836218221, 10)
    # print("closest items: ", closest_items)
    # # find 6 recommendations for user 219459 after looking at book 552147729
    # recommended_items = find_k_recommended_items(user=219459,
    #                                              item=552147729,
    #                                              ratings=ratings)
    # print("recommended items:", recommended_items)
    # # randomly delete 20% of ratings, predict them. find accuracy of predictions
    # reduced_rf, deleted_values = delete_some_ratings(ratings)
    # correct_predictions = 0
    # for (uid, iid, rating) in deleted_values:
    #     pred_rating = predict_rating(user=uid,
    #                                  item=iid,
    #                                  ratings=ratings)
    #     if pred_rating == rating:
    #         correct_predictions += 1
    # nr_deleted_values = len(deleted_values)
    # accuracy = correct_predictions / nr_deleted_values
    # print("#deleted: ", nr_deleted_values, "accuracy: ", accuracy)
    #
    #
