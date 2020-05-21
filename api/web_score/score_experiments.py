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

            response = response['data']

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
# SKLEARN
# TODO: can estimate ecdf with miltidim, but getting cdf is tricky
# https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html
# https://scikit-learn.org/stable/auto_examples/neighbors/plot_kde_1d.html
# https://machinelearningmastery.com/probability-density-estimation/

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, QuantileTransformer, PowerTransformer, Normalizer
from sklearn.neighbors import KernelDensity
from matplotlib import pyplot as plt

# define the model pipeline
scaler = QuantileTransformer()
model = KernelDensity(bandwidth=0.75, kernel='gaussian')  # bandwidth is basically smoothness of the curve
model = Pipeline([('scale', scaler), ('fit', model)])

# fit
fit_data = data[['google_items', 'instagram_followers_mean']].fillna(0).values.astype('float')  # 'google_items', 'wikipedia_items', 'twitter_followers_mean', 'instagram_followers_mean'
model.fit(fit_data)
probs = np.exp(model.score_samples(np.atleast_2d(fit_data)))
print(probs)

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.nquad.html
# TODO: this is too slow
from scipy import integrate
def f_kde(a, b):
    fit_data_ = np.atleast_2d([a, b])
    return np.exp(model.score_samples(np.atleast_2d(fit_data_)))
integrate.nquad(f_kde, [[0, 10],[0, 10]])

# plot
x, y = np.mgrid[0:1000:100j, 0:1000:100j]
probs = np.exp(model.score_samples(np.atleast_2d(np.vstack([x.ravel(), y.ravel()]).T)))
f = np.reshape(probs.T, x.shape)
plt.contourf(x, y, f, 20, cmap='Blues')
plt.plot(probs)

# ------------ #

import scipy.stats
kde = scipy.stats.gaussian_kde(fit_data.T)
probabilities = kde.pdf(fit_data.T)

kde.evaluate(np.atleast_2d([[16400, 213.6], [16400, 5000.6]]))

my_area = 0
my_area_values = []
for i in range(1,probabilities.shape[0]):
    my_area += 0.5*(probabilities[i] + probabilities[i-1])*(fit_data[i,0] - fit_data[i-1,0])
    my_area_values.append(my_area)

# ----------- #
# STATSMODELS
# TODO: simple yet can not do with multiple
# TODO: as for now lets combine a couple of these and do an average
from statsmodels.distributions.empirical_distribution import ECDF

ecdf = ECDF(fit_data.ravel())
plt.plot(ecdf.x, ecdf.y)
plt.plot(ecdf.x, (ecdf.y - 0.5) * 2)

ecdf(145)

# ----------- #
# https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/
# https://www.statsmodels.org/dev/generated/statsmodels.nonparametric.kernel_density.KDEMultivariate.html
from statsmodels.nonparametric.kernel_density import KDEMultivariate

fit_data = data[['google_items', 'wikipedia_items', 'twitter_followers_mean', 'instagram_followers_mean']].fillna(0).values.astype('float')  # 'google_items', 'wikipedia_items', 'twitter_followers_mean', 'instagram_followers_mean'
ecdf = KDEMultivariate(data=fit_data, var_type='u'*fit_data.shape[-1], bw=[1]*fit_data.shape[-1])  # bw=0.2 * np.ones_like(fit_data)
ecdf.cdf(fit_data[0, :])
ecdf.cdf([0, 0, 0, 1])
ecdf.cdf([0, 1, 0, 0])