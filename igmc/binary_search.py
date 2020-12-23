
def find_index(elements, val):
    first = 0
    last = len(elements) -1
    middle = (first + last) // 2

    if elements[middle] >= val:
        first = middle
    else:
        last = middle - 1

    return first, last

def binary_search(elements, val):
    """
    Performs a binary search over a set of elements
    to find the interval in which a value lies.

    Parameters
    ----------

    elements : Iterable
        Set of items to search

    val : Iterable type
        Query value
    """

    if val < elements[0] and val > elements[-1]:
        return None

    i, j = find_index(elements, val)

    while (j - i) > 1:
        i, j = find_index(elements[i:j], val)

    return i
