import reducebykey as reduce
import utils

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

# P(s_i) = count(s_i, w_j)/count(w_j)
P_s = {}
for ws in count_ws:
    for w in count_w:
        if ws[0][0] == w[0]:
            P_s[ws[0][1]] = ws[1]/w[1]
utils.print_to_file('P_s.json', P_s)

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

# P(f_j|s) = count(f_j, s)/count(s)
P_fs = {}
for s in count_s:
    temp = {}
    for fs in count_fs:
        if fs[0][0] == s[0]:
            # P(s_i)
            temp[fs[0][1]] = min(fs[1] / s[1], 1)
    P_fs[s[0]] = temp
utils.print_to_file('P_fs.json', P_fs)


count_text = 0
print("Computing senses of words")
utils.print_progress_bar(0, len(corpus), prefix='Progress:', suffix='Complete', length=50)
i = 0
# Foreach word, decide which sense is the best
# argmax(s in S) P(s)PROD_j(P(f_j|s))
for text in corpus:
    for sentence in text:
        for word in filter(lambda x: x['sense'] != '', sentence):
            # print("Word", word['lemma'])
            argmax_sense = "Unavailable"
            argmax_value = 0
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
                            # print("---", feature_in_sentence['lemma'], product)
                    # print("- P(s)", P_s[possible_sense])
                    # print("- PROD_j(P(f_j|s))", product)
                    if argmax_value < P_s[possible_sense]*product:
                        argmax_value = P_s[possible_sense]*product
                        argmax_sense = possible_sense
            except KeyError:
                print('KeyError: ' + word['lemma'])
            answers += 1
            if word['sense'] == argmax_sense:
                correct_answers += 1
            else:
                print(word['lemma'], argmax_sense, word['sense'] == argmax_sense)
        i += 1
        utils.print_progress_bar(i, len(corpus), prefix='Progress:', suffix='Complete', length=50)
print("Correct results:", correct_answers, "/", answers)
print("Accuracy: " + str(round(correct_answers/answers*100, 2)) + "%")
