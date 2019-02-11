# From https://stackoverflow.com/questions/48170666/how-to-get-the-gloss-given-sense-key-using-nltk-wordnet

import re
from nltk.corpus import wordnet as wn

sense_key_regex = r"(.*)\%(.*):(.*):(.*):(.*):(.*)"
synset_types = {1: 'n', 2: 'v', 3: 'a', 4: 'r', 5: 's'}


def synset_from_sense_key(sense_key):
    lemma, ss_type, lex_num, lex_id, head_word, head_id = re.match(sense_key_regex, sense_key).groups()
    ss_idx = '.'.join([lemma, synset_types[int(ss_type)], lex_id])
    return wn.synset(ss_idx)

# x = "art%1:09:00::"
# synset = synset_from_sense_key(x)

# print(synset.lemmas()[0].name() + ": " + synset.definition())