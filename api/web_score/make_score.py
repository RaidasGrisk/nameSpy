import os
import json
import pandas as pd
import numpy as np

from statsmodels.distributions.empirical_distribution import ECDF
import pickle

# pandas print options
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199
pd.set_option('display.width', None)  # or 199


class Scorer:
    def __init__(self):
        self.model = None


    def fit(self, data):
        self.model = ECDF(data.ravel())
        model_values = self.model.x
        self.middle_value = model_values[int(len(model_values)/2)]


    def scale(self, value):
        """
        Given that input is cumulative prob of a value,
        returns a score ranging from -1 to 1, where 0 is an average score (i.e. probability = 0.5)
        """
        return (value - 0.5) * 2

    def score(self, value):
        return self.scale(self.model(value))


    def plot(self, label):
        import pylab as plt
        plt.figure(label)
        mask = (0 < self.scale(self.model.y)) & (self.scale(self.model.y) < 1)
        plt.plot(self.model.x[mask], self.scale(self.model.y)[mask])


def data_restructure(response):
    response_ = {}

    response_['google_items'] = response['google']['items']
    response_['wikipedia_items'] = response['wikipedia']['items']

    response_['twitter_users'] = response['twitter']['num_users']
    response_['twitter_followers_first'] = [response['twitter']['users'][0].get('followers_count', np.nan) if response['twitter']['users'] else np.nan][0]
    response_['twitter_followers_mean'] = np.nanmean([i.get('followers_count', np.nan) for i in response['twitter']['users']])
    response_['twitter_followers_max'] = np.nanmax([i.get('followers_count', np.nan) for i in response['twitter']['users']] + [np.nan])

    response_['instagram_users'] = response['instagram']['num_users']
    response_['instagram_followers_first'] = [response['instagram']['users'][0].get('followers_count', np.nan) if response['instagram']['users'] else np.nan][0]
    response_['instagram_followers_mean'] = np.nanmean([i.get('followers_count', np.nan) for i in response['instagram']['users']])
    response_['instagram_followers_max'] = np.nanmax([i.get('followers_count', np.nan) for i in response['instagram']['users']] + [np.nan])
    return response_


def get_score(scorer_dict, json):
    input_values = data_restructure(json)
    scores = {}
    output_keys = ['google', 'wiki', 'twitter', 'ig']
    for scorer_item, output_key in zip(scorer_dict.keys(), output_keys):
        value = 0 if np.isnan(input_values[scorer_item]) else input_values[scorer_item]
        score = scorer_dict[scorer_item].score(value)
        scores[output_key] = score
    scores['web_score'] = sum(scores.values()) / len(scores.values())

    # post process
    scores = {k: np.around(scores[k], 2) for k in ['web_score'] + output_keys}

    return scores


def train_models():

    # ----------- #
    # load and structure
    finished_names = [i for i in os.listdir('web_score/data/resp')]
    data = pd.DataFrame()
    for name in finished_names:
        with open('web_score/data/resp/{}'.format(name)) as f:
            response = json.load(f)
            # how do we check if there's enough data to calc the score?
            if 'google' not in response.keys():
                continue
            response_ = data_restructure(response)
            data = data.append(pd.DataFrame(response_, index=[0]))

    # -------- #
    # make scorer object
    scorer_dict = {}
    for value in ['google_items', 'wikipedia_items', 'twitter_followers_mean', 'instagram_followers_mean']:
        scorer_dict[value] = Scorer()
        scorer_dict[value].fit(data[value].dropna().ravel())
        print(value, scorer_dict[value].score(0))
        scorer_dict[value].plot(label=value)

    # save
    with open('web_score/scorers/scorer_dict.pkl', 'wb') as f:
        pickle.dump(scorer_dict, f)

    # load
    # with open('web_score/scorers/scorer_dict.pkl', 'rb') as f:
    #     scorer_dict = pickle.load(f)


# test
# input1 = {'input': 'Rob Koskan',
#           'google': {'items': 77},
#           'wikipedia': {'items': 0, 'wordcount': 0},
#           'twitter': {'num_users': 0, 'users': []},
#           'instagram': {'num_users': 1, 'users': [{'username': 'rmkoskan', 'followers_count': 104, 'following_count': 67, 'posts_count': 158}]}}
#
# input2 = {'input': 'Rob Koskan',
#           'google': {'items': 0},
#           'wikipedia': {'items': 0, 'wordcount': 0},
#           'twitter': {'num_users': 0, 'users': []},
#           'instagram': {'num_users': 1, 'users': [{'username': 'rmkoskan', 'followers_count': 104, 'following_count': 67, 'posts_count': 158}]}}
#
# input3 = {'input': 'Rob Koskan',
#           'google': {'items': 400},
#           'wikipedia': {'items': 0, 'wordcount': 0},
#           'twitter': {'num_users': 0, 'users': [{'username': 'rmkoskan', 'followers_count': 104, 'following_count': 67, 'posts_count': 158}]},
#           'instagram': {'num_users': 1, 'users': [{'username': 'rmkoskan', 'followers_count': 104, 'following_count': 67, 'posts_count': 158}]}}
#
#
# get_score(scorer_dict, input3)