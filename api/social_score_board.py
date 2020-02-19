from main import get_social_score
import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

people = [
    'Elon Musk',
    'Albert Einstein',
    'Nicki Minaj',
    'Charles Darwin',
    'Bart Simpson',
    'Karolina Meschino',
    'Guido van Rossum',
    'Evan You',
    'Agnė Širinskienė',
    'Karolina Zivkovic',
    'Oleksii Potiekhin'
]

results = []
for person in people:
    score = get_social_score(person)
    results.append(score)

results_df = []
for person in results:
    person_details = [person['input_raw'],
                      person['google']['items'],
                      person['wikipedia']['totalhits'],
                      person['twitter']['num_users'],
                      [person['twitter']['users'][0]['followers_count'] if len(person['twitter']['users']) > 0 else 0][0],
                      person['instagram']['num_users'],
                      [person['instagram']['users'][0]['followers_count'] if len(person['instagram']['users']) > 0 else 0][0]
                      ]
    results_df.append(person_details)

df = pd.DataFrame(results_df, columns=['person', 'google_items', 'wiki_items', 'twtr_users', 'twtr_followers', 'ig_users', 'ig_followers'])
df.to_csv('social_score_board.csv', index=False)
print(df)

# output for web
import json

output = {'data': list(df.T.to_dict().values())}
with open('SocialScoreBoard.json', 'w') as fp:
    json.dump(output, fp, indent=2)

