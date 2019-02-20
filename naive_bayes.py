from xml.dom import minidom
import reducebykey as reduce
import synset_from_sense_key as sk
import utils as ut


def get_sense_key(instance_id):
    inputfile = open('WSD_Evaluation_Framework/Training_Corpora/SemCor/semcor.gold.key.txt')
    for line in inputfile:
        if line.split(" ")[0] == instance_id:
            return line.split(" ")[1][:-1]
    # inputfile.close()


corpus = minidom.parse('WSD_Evaluation_Framework/Training_Corpora/SemCor/semcor_one_text.data.xml')

texts = corpus.getElementsByTagName('text')

allsentences = []
allwords = []
allwords_with_sensekey = []
for text in texts:
    # print("\nText " + text.attributes['id'].value)
    sentences = text.getElementsByTagName('sentence')
    i = 0
    for sentence in sentences:
        # print("\nSentence " + sentence.attributes['id'].value)
        allwords_with_sensekey.append([])
        for item in sentence.childNodes:
            if item.nodeType == item.ELEMENT_NODE:
                allwords.append(item.attributes["lemma"].value)
                if item.hasAttribute("id"):
                    allwords_with_sensekey[i].append([item.attributes["lemma"].value, get_sense_key(item.attributes["id"].value)])
                else:
                    allwords_with_sensekey[i].append([item.attributes["lemma"].value, ''])
        allwords.append("\n") # End Of Sentence
        i = i+1
        # print("\n")

    print(" ".join(allwords))
    print(allwords_with_sensekey)

    # Count all occurrencies of a word in the given text
    # count(w_j)
    count_w = list(map(lambda w: (w, 1), allwords))
    count_w = list(reduce.reduceByKey(lambda x, y: x + y, count_w))
    count_w.sort(key=lambda x: x[0], reverse=True)
    #print(count_w)

    # Count all occurrencies of a (word, sense) in the given text
    # count(s_i, w_j)
    count_ws = list(map(lambda w: (w, 1), filter(lambda w: w[1] != '', ut.matrix_to_array(allwords_with_sensekey))))
    count_ws = list(reduce.reduceByKey(lambda x, y: x + y, count_ws))
    count_ws.sort(key=lambda x: x[1], reverse=True)
    #print(count_ws)

    # P(s_i) = count(s_i, w_j)/count(w_j)
    for ws in count_ws:
        for w in count_w:
            if ws[0][0] == w[0]:
                # P(s_i)
                p = ws[1]/w[1]
                #print("P(" + ws[0][1] + ") = " + str(p))


    # Count all occurrencies of a sense in the given text
    # count(w_j)
    count_s = list(map(lambda w: (w[1], 1), filter(lambda w: w[1] != '', ut.matrix_to_array(allwords_with_sensekey))))
    count_s = list(reduce.reduceByKey(lambda x, y: x + y, count_s))
    count_s.sort(key=lambda x: x[1], reverse=True)
    print(count_s)

    # Count all occurrencies of a (feature, sense) in the given text
    # count(f_j, s_i)
    count_fs = list()
    for sentence in allwords_with_sensekey:
        for sense in filter(lambda w: w[1] != '', sentence):
            for feature in filter(lambda w: w[1] != '', sentence):
                if sense != feature:
                    count_fs.append([sense[1], feature[0]])
    count_fs = list(map(lambda w: (w, 1), count_fs))
    count_fs = list(reduce.reduceByKey(lambda x, y: x + y, count_fs))
    print(count_fs)

    # P(f_j|s) = count(f_j, s)/count(s)
    for fs in count_fs:
        for s in count_s:
            if fs[0][0] == s[0]:
                # P(s_i)
                p = fs[1] / s[1]
                print("P(" + fs[0][1] + "|" + s[0] + ") = " + str(p))
