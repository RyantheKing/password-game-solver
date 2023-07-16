import csv


# noinspection PyTypeChecker
def load_elements_csv() -> tuple[tuple[str, int]]:
    """
    Load the CSV of periodic table element data

    :return: tuple of 2-tuples, each one containing the atomic symbol and atomic number, in that order
    """

    FILENAME = 'periodic_table.csv'

    with open(FILENAME) as csv_file:
        reader = csv.DictReader(csv_file)

        return tuple((row['Symbol'], int(row['AtomicNumber'])) for row in reader)


def safe_elements() -> tuple[tuple[str, int]]:
    """
    Load the CSV and filter out elements that start with a Roman numeral

    :return: the same thing as load_elements_csv but fewer elements
    """

    ROMAN_NUMERALS = set('IVXLCDM')

    return tuple(filter(lambda element: element[0][0] not in ROMAN_NUMERALS, load_elements_csv()))


def binary_search(arr: tuple[tuple[str, int]], query: int) -> tuple[str, int]:
    """
    Binary search to find le needed element

    :param arr: the array (actually a tuple) of elements
    :param query: the atomic number to find
    :return: the element if an exact match is found, the largest underestimate if one wasn't found
    """

    left = 0
    right = len(arr)

    while left < right:
        mid = (left + right) // 2
        element = arr[mid]

        if element[1] == query:
            return element
        elif element[1] < query:
            left = mid + 1
        else:
            right = mid

    return arr[left - 1]  # always return the underestimate


def required_elements(required_sum) -> list[tuple[str, int]]:
    """
    Get the greedily shortest list of elements whose atomic numbers sum up to the requirement

    :param safes: the elements that are safe
    :param required_sum: the sum that is required
    :return: the list of elements to use to get to that sum
    """

    safes = safe_elements()

    elements = []

    while required_sum > 0:
        symbol, atom_num = result = binary_search(safes, required_sum)

        required_sum -= atom_num

        elements.append(result)

    return elements


def test_elements():
    """
    testing function
    """

    safes = safe_elements()

    for safe in safes:
        print(safe)

    print()

    longest = 0

    for og_req in range(0, 201):
        elements = required_elements(og_req)

        print(f'{og_req}: {elements}')

        assert (sum(map(lambda e: e[1], elements)) == og_req)

        if len(elements) > longest:
            longest = len(elements)

    print()
    print(longest)

# test_elements()
