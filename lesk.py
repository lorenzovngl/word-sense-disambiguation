from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
import utils
import nlp_utils

answers = 0
correct_answers = 0
nltk_correct_answers = 0

corpus = utils.read_from_file('corpus.json')

for text in corpus[:1]:
    for sentence in text:
        for word in filter(lambda w: w['sense'] != '', sentence):
            max_overlap = 0
            best_sense = "Unavailable"
            context = list(map(lambda w: w['lemma'], filter(lambda w: w['sense'] != '' and w['lemma'] != word['lemma'], sentence)))
            # print("Target sense:", word['sense'])
            for synset in wn.synsets(word['lemma']):
                definition = set(synset.definition().split(' '))
                examples = set(utils.matrix_to_array([x.split(' ') for x in synset.examples()]))
                definition = set(definition.union(examples))
                definition = set(nlp_utils.remove_punctuation(s) for s in definition)
                if len(definition.intersection(set(context))) > max_overlap:
                    max_overlap = len(definition.intersection(set(context)))
                    best_sense = synset.lemmas()[0].key()
            # print("Best sense:", best_sense)
            # print("Lesk:", lesk(" ".join(context), word["lemma"]).lemmas()[0].key())
            answers += 1
            if best_sense == word['sense']:
                correct_answers += 1
            if lesk(" ".join(context), word["lemma"]).lemmas()[0].key() == word['sense']:
                nltk_correct_answers += 1

print("My Lesk")
print("Correct results:", correct_answers, "/", answers)
print("Accuracy: " + str(round(correct_answers/answers*100, 2)) + "%")
print("NLTK Lesk")
print("Correct results:", nltk_correct_answers, "/", answers)
print("Accuracy: " + str(round(nltk_correct_answers/answers*100, 2)) + "%")
