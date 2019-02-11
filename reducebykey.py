# From https://gist.github.com/Juanlu001/562d1ec55be970403442

from functools import reduce
from itertools import groupby


def reduceByKey(func, iterable):
    """Reduce by key.

    Equivalent to the Spark counterpart
    Inspired by http://stackoverflow.com/q/33648581/554319

    1. Sort by key
    2. Group by key yielding (key, grouper)
    3. For each pair yield (key, reduce(func, last element of each grouper))

    """
    get_first = lambda p: p[0]
    get_second = lambda p: p[1]
    # iterable.groupBy(_._1).map(l => (l._1, l._2.map(_._2).reduce(func)))
    return map(
        lambda l: (l[0], reduce(func, map(get_second, l[1]))),
        groupby(sorted(iterable, key=get_first), get_first)
    )


if __name__ == '__main__':
    # Example from https://www.safaribooksonline.com/library/view/learning-spark/9781449359034/ch04.html#idp7549488
    data = [(1, 2), (3, 4), (3, 6)]
    expected_result = [(1, 2), (3, 10)]
    assert list(reduceByKey(lambda x, y: x + y, data)) == expected_result