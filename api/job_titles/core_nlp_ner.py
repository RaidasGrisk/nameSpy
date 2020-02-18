from stanfordnlp.server import CoreNLPClient
from helpers import get_domain_from_url
import os

os.environ["CORENLP_HOME"] = os.getcwd() + '/stanford-corenlp-full-2018-02-27'
props = {"ner.applyFineGrained": "true", "ner.useSUTime": "false"}
annotators = ['ner']

core_nlp_client = CoreNLPClient(properties=props,
                                annotators=annotators,
                                timeout=9000,
                                memory='2G',
                                # output_format="text",    ## `outputFormat`, if used in `props` file
                                threads='7',
                                be_quiet=True)

print('loading NLP client in JAVA', core_nlp_client.annotate('test'))


def get_job_titles(google_data):

    def get_stanford_antities(text):
        # text = 'Elon Reeve Musk FRS is an engineer and technology entrepreneur. He is a citizen of South Africa'
        ann = core_nlp_client.annotate(text)
        entities = {}
        for sentence in ann.sentence:
            for mention in sentence.mentions:
                if mention.ner != 'O':
                    if mention.ner in entities.keys():
                        entities[mention.ner].add(mention.entityMentionText)
                    else:
                        entities[mention.ner] = set([mention.entityMentionText])
        # reformat to list instead of sets
        for key in entities:
            entities[key] = list(entities[key])
        return entities

    titles_parsed = []
    for item in google_data['items']:
        title_parsed = {}
        entities = get_stanford_antities(text=item['title'] + '. ' + item['snippet'])
        if 'TITLE' in entities.keys():
            job_titles = entities['TITLE']
            source = get_domain_from_url(item['displayLink'])
            title_parsed[source] = job_titles
            titles_parsed.append(title_parsed)

    return titles_parsed
