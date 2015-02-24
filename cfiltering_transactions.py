__author__ = 'niklas'

import os
import pandas as pd
import math


def euclidean_distance(series_tuple):
    s1, s2 = series_tuple



def calc_distances_euclidean(ratings, base_uid):
    """
    Calculate Euclidean distances of other users to user indicated by base_uid
    Distance = Eucl. dist. between vectors of (shared) ratings
    :param ratings: ratings transactions frame
    :param base_uid: compare other users ot this
    :return: pd.Series, index = uid, data = distance to base_uid
    """
    base_user_ratings = ratings[ratings["user"] == base_uid]
    base_user_ratings = base_user_ratings.set_index("item")
    base_user_ratings = base_user_ratings["rating"]
    other_ratings = ratings[ratings["user"] != base_uid]
    other_ratings = other_ratings.set_index("item")
    other_ratings = other_ratings["rating"]
    euclidean_distance(base_user_ratings.align(other_ratings, join="inner"))
    return ret_series


def load_rating_data():
    data_path = os.path.join("data", "BX-CSV-Dump", "BX-Book-Ratings.csv")
    ratings = pd.io.parsers.read_csv(data_path, sep=";", encoding="latin1")
    ratings.columns = ["user", "item", "rating"]
    return ratings


def find_k_closest_users(ratings, param, param1):
    pass


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
    # find 10 closest items to 836218221
    closest_items = find_k_closest_items(ratings, 836218221, 10)
    print("closest items: ", closest_items)
    # find 6 recommendations for user 219459 after looking at book 552147729
    recommended_items = find_k_recommended_items(user=219459,
                                                 item=552147729,
                                                 ratings=ratings)
    print("recommended items:", recommended_items)
    # randomly delete 20% of ratings, predict them. find accuracy of predictions
    reduced_rf, deleted_values = delete_some_ratings(ratings)
    correct_predictions = 0
    for (uid, iid, rating) in deleted_values:
        pred_rating = predict_rating(user=uid,
                                     item=iid,
                                     ratings=ratings)
        if pred_rating == rating:
            correct_predictions += 1
    nr_deleted_values = len(deleted_values)
    accuracy = correct_predictions / nr_deleted_values
    print("#deleted: ", nr_deleted_values, "accuracy: ", accuracy)


