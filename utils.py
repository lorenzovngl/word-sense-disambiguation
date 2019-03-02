import json


# Transforms [[["a","b"], ["c","d"]], [["e","f"], ["g","h"]]] to [["a","b"], ["c","d"], ["e","f"], ["g","h"]]
def matrix_to_array(matrix):
    array = []
    for line in matrix:
        for item in line:
            array.append(item)
    return array


def print_to_file(filename, data):
    f1 = open('dumps/' + filename, 'w+')
    f1.write(json.dumps(data, indent=4))
    f1.close()


def read_from_file(filename):
    f1 = open('dumps/' + filename, 'r+')
    data = json.load(f1)
    f1.close()
    return data


def iff(a, b, c):
    if a:
        return b
    else:
        return c


# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()
