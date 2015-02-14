import os

__author__ = 'niklas'

import pandas as pd
import math

def calc_item_distance_cosine(ratings_frame, iid):
    """
    calculate distances for other items from the one specified in iid
    :param ratings_frame: pandas frame, index = itemID, columns = users
    :param iid: item id
    :return: pd series, index = item id, value = distance
    """
    rf_trans = ratings_frame.transpose()
    item_ratings = rf_trans[iid]
    raise NotImplementedError

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


def load_rating_data():
    data_path = os.path.join("data", "BX-CSV-Dump", "BX-Book-Ratings.csv")
    ratings = pd.io.parsers.read_csv(data_path, sep=";", encoding="latin1")
    books = ratings["ISBN"].unique()
    users = ratings["User-ID"].unique()
    ratings_dict = {user: {} for user in users}
    for isbn in books:
        print("processing book", isbn)
        for user_id in users:
            print("processing user", user_id)
            rating = ratings[(ratings["ISBN"] == isbn) & (ratings["User-ID"] == user_id)]
            rating = rating["Book-Rating"]
            if len(rating) > 0:
                rating = rating[0]
                ratings_dict[user_id][isbn] = rating
    return pd.DataFrame(ratings_dict)

def find_k_closest_items(ratings_frame, param, param1):
    pass


def find_k_recommended_items(user, item, ratings_frame):
    pass


def delete_some_ratings(ratings_frame):
    pass


def predict_rating(user, item, ratings_frame):
    pass


if __name__ == "__main__":
    # load data
    print("loading data")
    ratings_frame = load_rating_data()
    print("done loading data")
    # find 10 closest users
    closest_users = find_k_closest_users(ratings_frame, 170155, 10)
    print("closest users:", closest_users)
    # find 10 closest items to 836218221
    closest_items = find_k_closest_items(ratings_frame, 836218221, 10)
    print("closest items: ", closest_items)
    # find 6 recommendations for user 219459 after looking at book 552147729
    recommended_items = find_k_recommended_items(user=219459,
                                                 item=552147729,
                                                 ratings_frame=ratings_frame)
    print("recommended items:", recommended_items)
    # randomly delete 20% of ratings, predict them. find accuracy of predictions
    reduced_rf, deleted_values = delete_some_ratings(ratings_frame)
    correct_predictions = 0
    for (uid, iid, rating) in deleted_values:
        pred_rating = predict_rating(user=uid,
                                     item=iid,
                                     ratings_frame=ratings_frame)
        if pred_rating == rating:
            correct_predictions += 1
    nr_deleted_values = len(deleted_values)
    accuracy = correct_predictions/ nr_deleted_values
    print("#deleted: ", nr_deleted_values, "accuracy: ", accuracy)