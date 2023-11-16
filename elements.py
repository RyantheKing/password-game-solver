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

        :param banned_chars: the set of banned characters
        :return: whether the number is safe
        """

        return self.symbol[0] not in ROMAN_NUMERALS and not (banned_chars and (self.characters & banned_chars))

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
    :return: the element index if an exact match is found, the largest underestimate if one wasn't found
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


def space_efficient_union(og: set[str], new_set: set[str]):
    if new_set <= og:
        return og
    else:
        return new_set | og


class ElementCombo:
    def __init__(self, elements: tuple[Element, ...] = (), atomic_num_total=0, char_count=0, char_set=None):
        self.elements = elements
        self.atomic_num_total = atomic_num_total
        self.char_count = char_count
        self.char_set = char_set or set()

    def __add__(self, other: Element) -> "ElementCombo":
        if isinstance(other, Element):
            chars_union = space_efficient_union(self.char_set, other.characters)

            return ElementCombo(elements=self.elements + (other,),
                                atomic_num_total=self.atomic_num_total + other.atomic_number,
                                char_count=self.char_count + len(other.symbol), char_set=chars_union)

        return NotImplemented

    @staticmethod
    def compare(combo_1: "ElementCombo", prospective_1: Element, combo_2: "ElementCombo", prospective_2: Element):
        chars_1 = combo_1.char_count + len(prospective_1.symbol)
        chars_2 = combo_2.char_count + len(prospective_2.symbol)

        if chars_1 != chars_2:
            return chars_1 - chars_2

        set_1_len = len(space_efficient_union(combo_1.char_set, prospective_1.characters))
        set_2_len = len(space_efficient_union(combo_2.char_set, prospective_2.characters))

        # return 0
        return set_1_len - set_2_len


def required_elements(required_sum: int, banned_chars: str = '', external_cache=None) -> ElementCombo:
    """
    Get the greedily shortest list of elements whose atomic numbers sum up to the requirement

    :param required_sum: the sum that is required
    :param banned_chars: the banned characters; NOT case-sensitive
    :param external_cache: an external cache that values will be stored in if provided
    :return: the list of elements to use to get to that sum
    """

    safes = Element.safe_elements(set(banned_chars.lower()) | set(banned_chars.upper()))

    return coinChange(safes, required_sum, external_cache=external_cache)


def coinChange(elements: tuple[Element], amount: int, external_cache=None):
    cache = [ElementCombo()]
    largest_atomic_num = max(map(lambda e: e.atomic_number, elements))
    end = 0

    if external_cache is not None:
        external_cache.append(cache[0])

    for target in range(1, amount + 1):
        minimum: ElementCombo | None = None
        minimum_element: Element | None = None

        for element in elements:
            # deque size is limited to the value of the largest coin, cuz that's the farthest we have to look back
            storage_location = (end - element.atomic_number) % len(cache)

            if element.atomic_number <= target:
                if cache[storage_location] is not None and \
                        (minimum is None or ElementCombo.compare(cache[storage_location], element, minimum,
                                                                 minimum_element) < 0):
                    minimum = cache[storage_location]
                    minimum_element = element
            else:
                break

        new_val = minimum + minimum_element if minimum is not None else None

        # limit the size of the deque to the value of the largest coin
        if target >= largest_atomic_num:
            cache[end] = new_val
            end = (end + 1) % len(cache)
        else:
            cache.append(new_val)

        if external_cache is not None:
            external_cache.append(new_val)

    last_combo = cache[(end - 1) % len(cache)]

    return last_combo


def required_elements_str(required_sum: int, banned_chars: str = '') -> str:
    """
    Like required_elements, but returns the elements as one conjoined string

    :param required_sum: the sum that is required
    :param banned_chars: the banned characters; NOT case-sensitive
    :return: the combined string of element symbols to use to get to that sum
    """

    return ''.join(map(lambda element: element.symbol, required_elements(required_sum, banned_chars).elements))


def generate_regex() -> re.Pattern:
    """
    Generate a regex to find all element symbols in the string, prioritizing 2-character symbols in case of overlap

    :return: the regex
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

    :return: the sum
    """

    regex = generate_regex()
    found = regex.findall(password)
    mapping = Element.symbols_to_atomic_nums

    return sum(map(lambda symbol: mapping[symbol], found))


def test_elements():
    """
    testing function
    """

    print(generate_regex())

    assert (len(Element.all_elements) == 118)
    assert (len(Element.symbols_to_atomic_nums) == 118)

    banned = ''

    safes = Element.safe_elements(set(banned.lower()) | set(banned.upper()))

    for safe in safes:
        print(safe)

    print()

    answers = []

    required_elements(200, banned_chars=banned, external_cache=answers)

    most_chars: ElementCombo | None = None
    most_unique_chars: ElementCombo | None = None

    for index in range(len(answers)):
        elements = answers[index]

        print(f'{index}: {elements and elements.elements}')

        if not elements:
            continue

        assert (sum(map(lambda e: e.atomic_number, elements.elements)) == index)

        if not most_chars or elements.char_count > most_chars.char_count:
            most_chars = elements

        if not most_unique_chars or len(elements.char_set) > len(most_unique_chars.char_set):
            most_unique_chars = elements

    print()
    print(f"Most chars: {most_chars.atomic_num_total} {most_chars.elements}")
    print(f"Most unique chars: {most_unique_chars.atomic_num_total} {most_unique_chars.elements}")
    print()


Element.load_elements_csv()

test_elements()
