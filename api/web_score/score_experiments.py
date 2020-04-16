import os
import json
import pandas as pd
import numpy as np

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

# https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html
# https://scikit-learn.org/stable/auto_examples/neighbors/plot_kde_1d.html

# https://machinelearningmastery.com/probability-density-estimation/
from sklearn.neighbors import KernelDensity
from matplotlib import pyplot

fit_data = data['google_items'].dropna().values.reshape(-1, 1)
fit_data = np.hstack((np.random.normal(loc=20, scale=5, size=100), np.random.normal(loc=40, scale=5, size=50))).reshape(-1, 1)
not_outlier = abs(fit_data - np.mean(fit_data)) < (2 * np.std(fit_data))
fit_data = fit_data[not_outlier].reshape(-1, 1)

model = KernelDensity(bandwidth=500, kernel='gaussian')  # bandwidth is basically smoothness of the curve
model.fit(fit_data)

np.exp(model.score_samples(np.array([-99999, 40, 99999]).reshape(-1, 1)))
np.exp(model.score(np.array([40]).reshape(-1, 1)))

probabilities = np.exp(model.score_samples(fit_data))
pyplot.hist(fit_data, bins=50, density=True)
pyplot.scatter(fit_data, probabilities, color='black', s=1, zorder=2)  # cmap='viridis'
pyplot.show()

# how to scale it to -1 to 1, where 0 is average person 1 is very well known?
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaler.fit(probabilities.reshape(-1, 1))
scaler.transform(np.exp([model.score(np.array([9999999]).reshape(-1, 1))]).reshape(-1, 1))


# ------------ #

import scipy.stats
kde = scipy.stats.gaussian_kde(fit_data.ravel())
probabilities = kde.pdf(fit_data.ravel())


my_area = 0
my_area_values = []
for i in range(1,probabilities.shape[0]):
    my_area += 0.5*(probabilities[i] + probabilities[i-1])*(fit_data[i,0] - fit_data[i-1,0])
    my_area_values.append(my_area)

# ----------- #
from statsmodels.distributions.empirical_distribution import ECDF

ecdf = ECDF(fit_data.ravel())
pyplot.plot(ecdf.x, ecdf.y)
pyplot.plot(ecdf.x, (ecdf.y - 0.5) * 2)

ecdf(145)
values = ecdf.__dict__['x']
middle_value = values[int(len(values)/2)]

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
        pyplot.plot(ecdf.x, ecdf.y)
        pyplot.plot(ecdf.x, self.scale(ecdf.y))


insta_scorer = Scorer()
insta_scorer.fit(fit_data)
insta_scorer.score(10000000)
insta_scorer.plot()

