from xml.dom import minidom
import utils


def get_sense_key(instance_id):
    inputfile = open('WSD_Evaluation_Framework/Training_Corpora/SemCor/semcor.gold.key.txt')
    for line in inputfile:
        if line.split(" ")[0] == instance_id:
            return line.split(" ")[1][:-1]
    # inputfile.close()


texts_to_parse = 10

corpus_dom = minidom.parse('WSD_Evaluation_Framework/Training_Corpora/SemCor/semcor.data.xml')
texts = corpus_dom.getElementsByTagName('text')
texts = texts[:texts_to_parse]

corpus = []
allsentences = []
allwords = []
allwords_with_sensekey = []
possible_senses = {}

print("Parsing corpus...")
utils.print_progress_bar(0, len(texts), prefix='Progress:', suffix='Complete', length=50)
i = 0
for text in texts[:10]:
    sentences = text.getElementsByTagName('sentence')
    j = 0
    for sentence in sentences:
        allwords_with_sensekey.append([])
        for item in sentence.childNodes:
            if item.nodeType == item.ELEMENT_NODE:
                allwords.append(item.attributes["lemma"].value)
                if item.hasAttribute("id"):
                    allwords_with_sensekey[j].append([item.attributes["lemma"].value, get_sense_key(item.attributes["id"].value)])
                else:
                    allwords_with_sensekey[j].append([item.attributes["lemma"].value, ''])
        allwords.append("\n") # End Of Sentence
        j += 1
    i += 1
    utils.print_progress_bar(i, len(texts), prefix='Progress:', suffix='Complete', length=50)

    allwords_with_sensekey_formatted = list(map(lambda w: {"word": w[0], "sense": w[1]}, filter(lambda w: w[1] != '', utils.matrix_to_array(allwords_with_sensekey))))
    corpus.append([[{"lemma": y[0], "sense": y[1]} for y in x] for x in allwords_with_sensekey])

    for x in allwords_with_sensekey_formatted:
        try:
            possible_senses[x['word']].append(x['sense'])
        except KeyError:
            possible_senses[x['word']] = [x['sense']]

    possible_senses_copy = possible_senses.copy()
    for key in possible_senses_copy.keys():
        possible_senses[key] = list(set(possible_senses[key]))

utils.print_to_file('allwords.json', allwords)
utils.print_to_file('allwords_with_sensekey.json', allwords_with_sensekey)
utils.print_to_file('possibile_senses.json', possible_senses)
utils.print_to_file('corpus.json', corpus)
