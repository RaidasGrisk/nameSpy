# datasets
# https://github.com/rootstrap/ai-job-title-area-classification/blob/master/data_process/data_sets/classified_titles.tsv
# https://github.com/rootstrap/ai-job-title-level-classification/blob/master/test_data/example_titles.csv
# https://github.com/afshinrahimi/jobdescription2jobtitle/blob/master/resources/Occupation%20Data.txt

import spacy
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

data = pd.read_csv('job_titles/Title_and_Salary_Listing.csv')
job_titles = data['Title Name'].tolist()
job_titles = [i.strip() for i in job_titles]
job_titles = job_titles + ['CEO', 'Chief Executive Officer']

nlp = spacy.load("en_core_web_md")
job_titles = [nlp(' '.join([str(t) for t in nlp(title) if not t.is_stop])) for title in job_titles]

text = 'Elon Musk is the Chief Engineer and CEO of Tesla having many obstacles not successding'
text = nlp(' '.join([str(t) for t in nlp(text) if not t.is_stop and t.pos_ in ['NOUN', 'PROPN']]))


# TODO: remove stop words
# TODO: look for nouns only?
# TODO: https://tfhub.dev/google/universal-sentence-encoder/4

output = []
for title in job_titles:
    sim = text.similarity(title)
    output.append([title, sim])

pd.DataFrame(output).sort_values(1).tail(20)

#################

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

text = ['View the profiles of people named Eglė Tauraitė. Join Facebook to connect with Eglė Tauraitė and others you may know. Facebook gives people the power to...', 'View the profiles of people named Egle Tauraite. Join Facebook to connect with Egle Tauraite and others you may know. Facebook gives people the power to...', 'Spruce Tauraitė. Project Coordinator at Lithuanian Biomass Energy Association. Lithuanian Biomass Energy Association LITBIOMAVilniaus ...', '+370624 86195th E. vilma.gaubyte@biokuras.lt mailbox. Spruce Tauraitė. Lithuanian Biomass Energy Association project coordinator. Ukmergės g.', "Companies Intelligent Medical Solutions, MB leader Tauraitė Spruce (Vilniaus r.). Information about the company's manual.", '2020-02-08 - Egle Taurasi, Project Coordinator at Lithuanian Biomass Energy Association. Egle has experience working with Lithuania ...', 'Egle Tauraitė - discover what lies under that name. Origin, photos, people involved.', 'Spruce Tauraitė - here you will find valuable information about your search term. Domek! Find out! Discuss!', 'Intelligent Medical Solutions, MB work specified the number of employees (insured). The number of employees. CEO: Spruce Tauraitė. Sodra data ...']
text = ['Elon Musk is the Chief Engineer and CEO of Tesla having many obstacles not successding']

with open('job_titles/job_titles_list.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
job_titles = [x.strip() for x in content]

job_matrix = embed(job_titles)
text_embed = embed(text)
np.inner(text_embed, job_matrix)
sim_matrix = np.inner(text_embed, job_matrix)

for item in range(sim_matrix.shape[0]):
    print(pd.DataFrame([job_titles, sim_matrix[item]]).T.sort_values(1))