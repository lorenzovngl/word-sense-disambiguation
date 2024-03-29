# From https://stackoverflow.com/questions/48170666/how-to-get-the-gloss-given-sense-key-using-nltk-wordnet

import re
from nltk.corpus import wordnet as wn
import string

sense_key_regex = r"(.*)\%(.*):(.*):(.*):(.*):(.*)"
synset_types = {1: 'n', 2: 'v', 3: 'a', 4: 'r', 5: 's'}


def synset_from_sense_key(sense_key):
    lemma, ss_type, lex_num, lex_id, head_word, head_id = re.match(sense_key_regex, sense_key).groups()
    ss_idx = '.'.join([lemma, synset_types[int(ss_type)], lex_id])
    return wn.synset(ss_idx)


def remove_punctuation(my_str):
    table = my_str.maketrans({key: None for key in string.punctuation})
    return my_str.translate(table)
