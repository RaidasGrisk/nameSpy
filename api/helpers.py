import re


def get_entities(input, nlp_models):

    # get all entities
    entities = {}
    for model_lang, nlp_model in nlp_models.items():
        doc = nlp_model(input)
        if doc.ents:
            for ent in doc.ents:
                ent_str = str(ent)
                # print(model_lang, ent.text, ent.label_)
                if ent.label_ in entities.keys():
                    entities[ent.label_].add(ent_str)
                else:
                    entities[ent.label_] = set([ent_str])
        else:
            print(model_lang, '-')

    # convert to decent dict
    for key, value in entities.items():
        entities[key] = list(value)

    return entities


def process_entities(entities):

    # analyze and return
    if 'PERSON' in entities.keys():

        if len(entities['PERSON']) > 1:
            print(entities['PERSON'])
            return list(entities['PERSON'])[0]
        else:
            return list(entities['PERSON'])[0]
    else:
        print('No manes here')
        return None


def get_domain_from_url(url):
    regex = '^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)'
    return re.search(regex, url)[0]
