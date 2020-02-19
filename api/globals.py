import spacy

nlp_models = {'LTU': spacy.load('lt_core_news_sm'),
              'EN': spacy.load('en_core_web_sm')}



# from stanfordcorenlp import StanfordCoreNLP
# import logging
# import json
#
# class StanfordNLP:
#     def __init__(self, host='http://localhost', port=9000):
#         self.nlp = StanfordCoreNLP(host, port=port, timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
#         self.props = {
#             'annotators': 'ner',
#             'pipelineLanguage': 'en',
#             'outputFormat': 'json',
#             "ner.applyFineGrained": "true",
#             "ner.useSUTime": "false"
#         }
#
#     def word_tokenize(self, sentence):
#         return self.nlp.word_tokenize(sentence)
#
#     def pos(self, sentence):
#         return self.nlp.pos_tag(sentence)
#
#     def ner(self, sentence):
#         return self.nlp.ner(sentence)
#
#     def parse(self, sentence):
#         return self.nlp.parse(sentence)
#
#     def dependency_parse(self, sentence):
#         return self.nlp.dependency_parse(sentence)
#
#     def annotate(self, sentence):
#         return json.loads(self.nlp.annotate(sentence, properties=self.props))
#
#     @staticmethod
#     def tokens_to_dict(_tokens):
#         tokens = defaultdict(dict)
#         for token in _tokens:
#             tokens[int(token['index'])] = {
#                 'word': token['word'],
#                 'lemma': token['lemma'],
#                 'pos': token['pos'],
#                 'ner': token['ner']
#             }
#         return tokens
#
# if __name__ == '__main__':
#     sNLP = StanfordNLP()
#     text = 'A blog post using Stanford CoreNLP Server. Visit www.khalidalnajjar.com for more details.'
#     print "Annotate:", sNLP.annotate(text)
#     print "POS:", sNLP.pos(text)
#     print "Tokens:", sNLP.word_tokenize(text)
#     print "NER:", sNLP.ner(text)
#     print "Parse:", sNLP.parse(text)
#     print "Dep Parse:", sNLP.dependency_parse(text)
#

# import nltk
# from nltk.tag.stanford import StanfordNERTagger
#
# sentence = 'Elon Reeve Musk FRS is an engineer and technology entrepreneur. He is a citizen of South Africa, Canada, and the '
#
# jar = './stanford-ner-2018-10-16/stanford-ner-3.9.2.jar'
# model = './stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz'
#
# # Prepare NER tagger with english model
# ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
#
# # Tokenize: Split sentence into words
# words = nltk.word_tokenize(sentence)
#
# # Run NER tagger on words
# print(ner_tagger.tag(words))

#
#
# from nltk.parse.corenlp import CoreNLPServer
# import os
#
# STANFORD = os.path.join("stanford-corenlp-full-2018-02-27")
# server = CoreNLPServer(
#    os.path.join(STANFORD, "stanford-corenlp-3.9.1.jar"),
#    os.path.join(STANFORD, "stanford-corenlp-3.9.1-models.jar"),
# )
#
# # Start the server in the background
# server.start()
#
# from nltk.parse.corenlp import CoreNLPDependencyParser
#
# parser = CoreNLPDependencyParser(tagtype='ner')
# parse = next(parser.raw_parse("Elon musk the CEO of tesla"))
# print(parse)

