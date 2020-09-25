"""
IsolationForest does not really fit the task as it will
assign an outlier score for very low numbers as well as
very high numbers. This does not work in this case.

Try VAE.

"""

import os
import json
import pandas as pd
import numpy as np
import dill

from statsmodels.distributions.empirical_distribution import ECDF
from sklearn.ensemble import IsolationForest
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline

import pickle

# pandas print options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)


# subclassing to add transform method otherwise,
# it is incompatible with pipeline logic
class CustomIsolationForest(IsolationForest):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transform(self, X):
        return self.decision_function(X)


# do not want to subclass ECDF because
# I do not understand how to combine sklearn and this mechanic:
# ecdf = ECDF([3, 3, 1, 4]); ecdf([3, 55, 0.5, 1.5])
# therefore just create a new class
class CustomECDF(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.models = []
        self.x_clean = None

    def fit(self, X, y=None):
        for col in X.columns:
            X_ = self.filter_outliers(X[col])

            # there are many data-points where
            # twitter / IG data is missing.
            # filling it with 0 screws the data by
            # making it look like having 10 followers is a lot.
            # drop data-points with values == -1
            # DROP IT ONLY DURING THE TRAINING
            # THIS MUST BE SYNCED WITH PREPROCESS PIPE FILL NA
            X_ = X_[X_ != -1]
            model = ECDF(X_)

            # exception:
            # due to weird wiki data where an unknown and an average name has 0 items
            # this has to be fixed manually. All probs where items <= 0 has prob of 0.5
            # meaning that names with 0 wiki items are average names.
            # There are no names that has score of -1.
            if col == 'wikipedia_items':
                model.y[model.x <= 0] = 0.5

            self.models.append(model)
            self.x_clean = X
        return self

    @staticmethod
    def filter_outliers(x):
        return x[x.between(x.quantile(.01), x.quantile(.99))]

    @staticmethod
    def scale(value):
        # Given that input is cumulative prob of a value,
        # returns a score ranging from -1 to 1,
        # where 0 is an average score (i.e. probability = 0.5)
        return (value - 0.5) * 2

    def transform(self, X):
        x_copy = pd.DataFrame()
        for model, col in zip(self.models, X.columns):
            x_copy[col] = self.scale(model(X[col]))
        x_copy = x_copy.round(2)
        return x_copy


def restructure_data(responses: list) -> list:
    """Takes in a list of response data jsons and outputs a list of restructured jsons"""
    responses_ = []
    for resp in responses:
        response_ = {
            'google_items': resp['google']['items'],
            'wikipedia_items': resp['wikipedia']['items'],
            # 'twitter_users': resp['twitter']['num_users'],
            # 'instagram_users': resp['instagram']['num_users'],
            'twitter_followers_mean': np.nanmean(
                [i.get('followers_count', np.nan) for i in resp['twitter']['users']]),
            'instagram_followers_mean': np.nanmean(
                [i.get('followers_count', np.nan) for i in resp['instagram']['users']])
        }
        responses_.append(response_)
    return responses_


def load_data():
    files = [i for i in os.listdir('web_score/data/resp')]
    data = []
    for file in files:
        with open('web_score/data/resp/{}'.format(file)) as f:
            response = json.load(f)
            if 'data' not in response.keys():
                continue
            data.append(response['data'])
    return data

if __name__ == '__main__':

    # 1. read jsons into a list
    data = load_data()

    # 2. clean data
    # can not do this inside the pipeline as doing so
    # might get rid of the input data during inference
    # if during the inference only part of data is received
    # this is to filter out some really bad responses, e.g.
    # 'instagram': {'num_users': 1, 'users': [{'username': 'charietakei'}]}
    for i in data:
        if i['instagram']['num_users'] > 0:
            if i['instagram']['users'][0].get('followers_count', -1) < 0:
                data.remove(i)

    # split the pipeline into two one for json and df
    # the other one for fillna and all the rest
    preprocess_pipe = Pipeline(
        [
            ('restructure_jsons', FunctionTransformer(restructure_data)),
            ('jsons_to_df', FunctionTransformer(lambda x: pd.DataFrame(x))),
            # not using imputer as it casts to array
            # fill with -1 to separate missing case from 0
            ('fillna', FunctionTransformer(lambda x: x.fillna(-1))),
        ]
    )

    model_pipe = Pipeline(
        [
            ('ECDF', CustomECDF()),
            # ('IF', CustomIsolationForest(n_estimators=5)),
            ('final_score', FunctionTransformer(lambda x:
                                                np.array(x)
                                                .reshape(x.shape[0], -1)
                                                .mean(axis=1)
                                                .round(2)))
        ]
    )

    # output
    train_data = preprocess_pipe.transform(data)
    model_pipe.fit(train_data)

    # scores = model_pipe.transform(train_data)
    # temp = pd.concat([train_data, pd.Series(scores)], axis=1)
    # temp.sort_values(0).round(2)

    # save
    print('Saving')
    preprocess_pipe_path = 'web_score/scorers/preprocess_pipe.pkl'
    model_pipe_path = 'web_score/scorers/model_pipe.pkl'
    with open(preprocess_pipe_path, 'wb') as i, open(model_pipe_path, 'wb') as j:
        dill.dump(preprocess_pipe, i)
        dill.dump(model_pipe, j)


def debugging():

    # load models
    preprocess_pipe_path = 'web_score/scorers/preprocess_pipe.pkl'
    model_pipe_path = 'web_score/scorers/model_pipe.pkl'
    with open(preprocess_pipe_path, 'rb') as i, open(model_pipe_path, 'rb') as j:
        preprocess_pipe = dill.load(i)
        model_pipe = dill.load(j)

    debug_data = {
        'google': {
            'items': 15500000
        },
        'wikipedia': {
            'items': 436,
        },
        'twitter': {
            'num_users': 0,
            'users': [
                {
                    'followers_count': np.mean([48843, 3688, 2450, 1792, 1860]),
                },
            ]
        },
        'instagram': {
            'num_users': 1,
            'users': [
                {
                    'followers_count': np.mean([1589, 293, 27675, 3688, 152])
                },

            ]
        }
    }

    # get scores
    preprocessed_data = preprocess_pipe.transform([debug_data])
    separate_scores = model_pipe.named_steps['ECDF'].transform(preprocessed_data).T[0].to_dict()
    final_score = {'web_score': model_pipe.transform(preprocess_pipe.transform([debug_data]))[0]}

    print({**final_score, **separate_scores})
