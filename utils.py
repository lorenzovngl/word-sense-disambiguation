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


def iff(a, b, c):
    if a:
        return b
    else:
        return c
