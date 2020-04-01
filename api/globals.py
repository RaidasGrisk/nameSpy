"""
https://stackoverflow.com/questions/13034496/using-global-variables-between-files
"""

import spacy

nlp_models = {'LTU': spacy.load('lt_core_news_sm'),
              'EN': spacy.load('en_core_web_sm')}
