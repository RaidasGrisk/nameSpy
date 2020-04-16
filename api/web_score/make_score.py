import os
import json
import pandas as pd
import numpy as np
import pylab as plt

# pandas print options
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199
pd.set_option('display.width', None)  # or 199

# ----------- #
# load and structure
finished_names = [i for i in os.listdir('web_score/data/resp')]

data = pd.DataFrame()
for name in finished_names:
    with open('web_score/data/resp/{}'.format(name)) as f:
        response = json.load(f)

        if response.get('input'):
            response_ = {}
            response_['input'] = [response['input']]
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

        data = data.append(pd.DataFrame.from_dict(response_))

# clean
data = data.set_index('input')
data = data.sort_index()

# -------- #
# make stats distributions

from statsmodels.distributions.empirical_distribution import ECDF
import pickle
import pylab as plt

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


    def plot(self):
        plt.plot(self.model.x, self.model.y)
        plt.plot(self.model.x, self.scale(self.model.y))


fit_data = data['google_items'].dropna().values.reshape(-1, 1)

insta_scorer = Scorer()
insta_scorer.fit(fit_data.ravel())
insta_scorer.score(220)
insta_scorer.plot()

# save
with open('web_score/scorers/insta_scorer.pkl', 'wb') as f:
    pickle.dump(insta_scorer, f)

# load
with open('web_score/scorers/insta_scorer.pkl', 'rb') as f:
    object = pickle.load(f)