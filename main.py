from xml.dom import minidom
import reducebykey as reduce
import synset_from_sense_key as sk


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
    for sentence in sentences:
        # print("\nSentence " + sentence.attributes['id'].value)
        for item in sentence.childNodes:
            if item.nodeType == item.ELEMENT_NODE:
                allwords.append(item.attributes["lemma"].value)
                if item.hasAttribute("id"):
                    allwords_with_sensekey.append([item.attributes["lemma"].value, get_sense_key(item.attributes["id"].value)])
            '''
                if item.hasAttribute("id"):
                    print(item.firstChild.nodeValue + " -> " + sk.synset_from_sense_key(get_sense_key(item.attributes["id"].value)).definition())
                else:
                    print(item.firstChild.nodeValue)'''
        allwords.append("\n") # End Of Sentence
        # print("\n")

    print(" ".join(allwords))

    # Count all occurrencies of a word in the given text
    count_w = list(map(lambda w: (w, 1), allwords))
    count_w = list(reduce.reduceByKey(lambda x, y: x + y, count_w))
    count_w.sort(key=lambda x: x[0], reverse=True)
    print(count_w)

    # Count all occurrencies of a (word, sense) in the given text
    count_ws = list(map(lambda w: (w, 1), allwords_with_sensekey))
    count_ws = list(reduce.reduceByKey(lambda x, y: x + y, count_ws))
    count_ws.sort(key=lambda x: x[0], reverse=True)
    print(count_ws)

    for ws in count_ws:
        for w in count_w:
            if ws[0][0] == w[0]:
                # P(s_i)
                s = ws[1]/w[1]
                print("P(" + ws[0][1] + ") = " + str(s))
