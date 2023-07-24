import csv
import collections
import re

ROMAN_NUMERALS = set('IVXLCDM')


class Element:
    all_elements: list['Element'] = []
    symbols_to_atomic_nums: dict[str, int] = {}

    def __init__(self, element_dict: dict[str, str]):
        """
        :param element_dict: the dict representing the element
        """

        self.symbol = element_dict['Symbol']
        self.characters = set(self.symbol)
        self.atomic_number = int(element_dict['AtomicNumber'])

        self.all_elements.append(self)
        self.symbols_to_atomic_nums[self.symbol] = self.atomic_number

    def safe(self, banned_chars: set[str]) -> bool:
        """
        Determine whether this element is safe (no roman numerals and no banned characters)

        :return: whether the number is safe
        """

        return self.symbol[0] not in ROMAN_NUMERALS and not (self.characters & banned_chars)

    @classmethod
    def load_elements_csv(cls):
        """
        Load the CSV of periodic table element data
        """

        FILENAME = 'periodic_table.csv'

        with open(FILENAME) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                cls(row)

    @classmethod
    def safe_elements(cls, banned_chars: set[str]) -> tuple['Element']:
        """
        Load the CSV and filter out elements that start with a Roman numeral

        :param banned_chars: the set of characters that cannot be used
        :return: a tuple of elements that are safe
        """

        return tuple(filter(lambda element: element.safe(banned_chars), cls.all_elements))

    def __str__(self):
        return f'{self.symbol} {self.atomic_number}'

    __repr__ = __str__


def binary_search(arr: tuple[Element], query: int, right: int) -> int:
    """
    Binary search to find le needed element

    :param arr: the array (actually a tuple) of elements
    :param query: the atomic number to find
    :param right: the right edge (not included)
    :return: the element if an exact match is found, the largest underestimate if one wasn't found
    """

    left = 0

    while left < right:
        mid = (left + right) // 2
        element = arr[mid]

        if element.atomic_number == query:
            return mid
        elif element.atomic_number < query:
            left = mid + 1
        else:
            right = mid

    return left - 1  # always return the underestimate


def required_elements(required_sum: int, banned_chars: str) -> list[Element]:
    """
    Get the greedily shortest list of elements whose atomic numbers sum up to the requirement

    :param required_sum: the sum that is required
    :param banned_chars: the banned characters
    :return: the list of elements to use to get to that sum
    """

    safes = Element.safe_elements(set(banned_chars.lower()) | set(banned_chars.upper()))

    elements = []

    right = len(safes)

    while required_sum > 0:
        result_index = binary_search(safes, required_sum, right)
        result = safes[result_index]

        required_sum -= result.atomic_number

        elements.append(result)

        right = result_index + 1

    return elements


def required_elements_str(required_sum: int, banned_chars: str) -> str:
    """
    Like required_elements, but returns the elements as one conjoined string
    """

    return ''.join(map(lambda element: element.symbol, required_elements(required_sum, banned_chars)))


def generate_regex() -> re.Pattern:
    """
    Generate a regex to find all element symbols in the string, prioritizing 2-character symbols in case of overlap
    """

    elements = Element.all_elements
    deque = collections.deque()

    for element in elements:
        if len(element.symbol) == 1:
            deque.append(element.symbol)
        else:
            deque.appendleft(element.symbol)

    return re.compile('|'.join(deque), flags=re.U)


def password_element_sum(password: str) -> int:
    """
    Get the sum of all element symbols in the given password
    """

    regex = generate_regex()
    found = regex.findall(password)
    mapping = Element.symbols_to_atomic_nums

    return sum(map(lambda symbol: mapping[symbol], found))


def test_elements():
    """
    testing function
    """

    banned = 'oge'

    safes = Element.safe_elements(set(banned.lower()) | set(banned.upper()))

    for safe in safes:
        print(safe)

    print()

    longest = 0

    for og_req in range(0, 201):
        elements = required_elements(og_req, banned)

        print(f'{og_req}: {elements}')

        assert (sum(map(lambda e: e.atomic_number, elements)) == og_req)

        if len(elements) > longest:
            longest = len(elements)

    print()
    print(longest)


Element.load_elements_csv()
