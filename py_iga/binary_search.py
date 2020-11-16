
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

    i, j = find_index(elements, val)

    while (j - i) > 1:
        i, j = find_index(elements[i:j], val)

    return i
