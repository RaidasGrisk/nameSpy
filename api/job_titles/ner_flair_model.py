from flair.inference_utils import WordEmbeddingsStore
from flair.data import Sentence

from helpers import get_domain_from_url
import pickle
import unicodedata

# load model
# model = pickle.load(open('job_titles/flair_model2.pickle', 'rb'))
# WordEmbeddingsStore.load_stores(model)

from flair.models import SequenceTagger
model = SequenceTagger.load('job_titles/flair_model.pt')


def get_flair_entities(input, score_threshold=0.9):

    sentence = Sentence(input, use_tokenizer=True)
    model.predict(sentence)

    # refactor flair output
    entities = []
    prev_end_pos = 0
    prev_entity_part = ''
    for entity in sentence.to_dict(tag_type='ner')['entities']:

        if entity['confidence'] < score_threshold:
            continue

        print(entity)
        if prev_end_pos + 1 == entity['start_pos']:
            del entities[-1]
            final_entity = prev_entity_part + ' ' + entity['text']
        else:
            final_entity = entity['text']

        entities.append(final_entity.strip())
        prev_end_pos = entity['end_pos']
        prev_entity_part += ' ' + entity['text']

    return entities


def get_job_titles(google_data, ner_threshold):

    titles_parsed = {}
    for item in google_data['items']:

        job_titles = get_flair_entities(item['title'], ner_threshold) + get_flair_entities(item['snippet'], ner_threshold)

        if job_titles:
            job_titles = [i.lower() for i in job_titles]
            job_titles = [''.join((c for c in unicodedata.normalize('NFD', i) if unicodedata.category(c) != 'Mn')) for i in job_titles]
            source = [get_domain_from_url(item['url']) if item['url'] else 'unknown'][0]
            for title in job_titles:
                if titles_parsed.get(title):
                    titles_parsed[title]['count'] += 1
                    titles_parsed[title]['sources'].add(source)
                else:
                    titles_parsed.update({title: {'count': 1, 'sources': {source}}})

    return titles_parsed
