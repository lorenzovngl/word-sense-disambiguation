# Transforms [[["a","b"], ["c","d"]], [["e","f"], ["g","h"]]] to [["a","b"], ["c","d"], ["e","f"], ["g","h"]]
def matrix_to_array(matrix):
    array = []
    for line in matrix:
        for item in line:
            array.append(item)
    return array
