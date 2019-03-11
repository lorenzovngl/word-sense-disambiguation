import random
import reducebykey as reduce
import utils
import functools as ft
from math import log

answers = 0
correct_answers = 0

allwords = utils.read_from_file('allwords.json')
allwords_with_sensekey = utils.read_from_file('allwords_with_sensekey.json')
possible_senses = utils.read_from_file('possibile_senses.json')
corpus = utils.read_from_file('corpus.json')

print("Counting occurrencies...")
# Count all occurrencies of a word in the corpus
# count(w_j)
count_w = list(map(lambda w: (w, 1), allwords))
count_w = list(reduce.reduceByKey(lambda x, y: x + y, count_w))
count_w.sort(key=lambda x: x[0], reverse=True)
utils.print_to_file('count_w.json', count_w)

# Count all occurrencies of a (word, sense) in the corpus
# count(s_i, w_j)
count_ws = list(map(lambda w: (w, 1), filter(lambda w: w[1] != '', utils.matrix_to_array(allwords_with_sensekey))))
count_ws = list(reduce.reduceByKey(lambda x, y: x + y, count_ws))
count_ws.sort(key=lambda x: x[1], reverse=True)
utils.print_to_file('count_sw.json', count_ws)

# Count all occurrencies of a sense in the corpus
# count(s_i)
count_s = list(map(lambda w: (w[1], 1), filter(lambda w: w[1] != '', utils.matrix_to_array(allwords_with_sensekey))))
count_s = list(reduce.reduceByKey(lambda x, y: x + y, count_s))
count_s.sort(key=lambda x: x[0], reverse=True)
utils.print_to_file('count_s.json', count_s)

# Count all occurrencies of a (feature, sense) in the corpus
# count(f_j, s_i)
count_fs = list()
for sentence in allwords_with_sensekey:
    for sense in filter(lambda w: w[1] != '', sentence):
        for feature in filter(lambda w: w[1] != '', sentence):
            if sense != feature:
                count_fs.append([sense[1], feature[0]])
count_fs = list(map(lambda w: (w, 1), count_fs))
utils.print_to_file('count_fs.json', count_fs)
count_fs = list(reduce.reduceByKey(lambda x, y: x + y, count_fs))

print("Initializing parameters...")
# Random initialization
# P(f_j|s_k) = count(f_j, s_k)/count(s_k)
P_fs = {}
for s in count_s:
    temp = {}
    for fs in count_fs:
        if fs[0][0] == s[0]:
            # P(s_i)
            temp[fs[0][1]] = random.uniform(0, 1)
    P_fs[s[0]] = temp
utils.print_to_file('P_fs.json', P_fs)

# Random initialization
# P(s_k) = count(s_k, w_j)/count(w_j)
P_s = {}
for ws in count_ws:
    for w in count_w:
        if ws[0][0] == w[0]:
            P_s[ws[0][1]] = random.uniform(0, 1)
utils.print_to_file('P_s.json', P_s)

# P(c_i|s_k) = PROD_{f_j in c_i) (P(f_j|s_k))
P_cs = []
for text in corpus:
    for i, sentence in enumerate(text):
        temp = {}
        for word in filter(lambda w: w['sense'] != '', sentence):
            try:
                for possible_sense in possible_senses[word['lemma']]:
                    # print("- Possible sense", possible_sense)
                    product = 1
                    for feature_in_sentence in filter(lambda w: w['sense'] != '' and w['lemma'] != word['lemma'], sentence):
                        # print("--", feature_in_sentence['lemma'])
                        found = False
                        for feature_in_senses in P_fs[possible_sense]:
                            if feature_in_sentence['lemma'] == feature_in_senses:
                                found = True
                                # print("---", feature_in_senses, P_fs[possible_sense][feature_in_senses])
                                product *= P_fs[possible_sense][feature_in_senses]
                                break
                        if not found:
                            product = 0
                    # print("P(c_" + str(i), "|", possible_sense, ") =", product)
                    temp[possible_sense] = product
            except KeyError:
                print('KeyError: ' + word['lemma'])
        P_cs.append(temp)
utils.print_to_file('P_cs.json', P_cs)

# P(c_i) = SUM P(c_i|s_k)P(s_k)
P_c = []
for context in P_cs:
    sum = 0
    for sense in context:
        sum += context[sense] * P_s[sense]
    P_c.append(sum)
utils.print_to_file('P_c.json', P_c)

# l(C) -> Likelihood of the corpus
sum_contexts = ft.reduce(lambda x, y: x*y, P_c)
likelihood = log(sum_contexts)
print(likelihood)

# E-step
# h_ik = P(c_i|s_k)/SUM(P(c_i|s_k)
h_ik = []
for i, context in enumerate(P_cs):
    temp = {}
    for sense in context:
        temp[sense] = P_cs[i][sense]/P_c[i]
    h_ik.append(temp)
utils.print_to_file('h_ik.json', h_ik)

# M-step
for sense in P_fs:
    sum = 0
    for feature in P_fs[sense]:
        for text in corpus:
            for i, sentence in enumerate(text):
                try:
                    if feature in [x['lemma'] for x in sentence]:
                        sum += h_ik[i][sense]
                except KeyError:
                    # TODO: Too much keyerrors, probably there is a bug
                    pass
                    # print('KeyError:', feature)
    print(sum)

