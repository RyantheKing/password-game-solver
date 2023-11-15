# generates password and make a few other calculations like the total sum for digits and elements
import data
import elements
import requests
from datetime import datetime
import pytz
import pylunar
from collections import defaultdict

def birth_paul():
    '''
    And he called to him two of the centurions and said,
    “Get two hundred soldiers ready by the third hour of the night to proceed to Caesarea, with seventy horsemen and two hundred spearmen.”
    They were also to provide mounts to put Paul on and bring him safely to Felix the governor.
    (change the egg in the string to a chicken)
    '''
    data.paul = '🐔'

def digit_sum(password : str):
    """
    Get the sum of all digits in the given password
    :param password: The password to sum
    :return: The sum of all digits in the password
    """
    return sum([int(num) for num in password if num.isdigit()])

def get_wordle_answer() -> str:
    """
    API call to get the wordle answer
    :return: The wordle answer
    """
    # uses requests library
    response = requests.get("https://neal.fun/api/password-game/wordle?date=" + datetime.today().strftime("%Y-%m-%d"))
    return response.json()['answer']

def get_time():
    """
    Gets the time in HH:MM format
    """
    return datetime.now().strftime("%I:%M")

def sum_25(password: str) -> str:
    """
    Print out a string to compensate for the missing digits in the password
    :param password: The password with digits in it to compensate for
    :return: The string to add to the password
    """
    diff = 25 - digit_sum(password)
    return_str = ""
    while diff > 9:
        return_str += "9"
        diff -= 9
    return_str += str(diff)
    return return_str

def get_element_string(password: str, banned_chars='') -> str:
    """
    Gets the string of elements to add to the password to make a total atomic number of 200
    :param password: The password containing pre-existing elements
    :return: The string of elements to add to the password
    """
    return elements.required_elements_str(200 - elements.password_element_sum(password), banned_chars=banned_chars)

def dot_string(password: str) -> str:
    """
    Gets the string of dots to add to the password to make a total length of 101
    :param password: The password
    :return: The string of dots to add to the password
    """
    length = 101-password_length(password)
    return '.,'*(length//2) + '.'*(length%2)

def password_length(password: str) -> int:
    """
    Gets the length of the password without the invisible characters. DO NOT USE 'len(password)'
    :param password: The password
    :return: The length of the password without the invisible characters
    """
    return len([char for char in password if ord(char) not in [65039, 8205, 9794]])

def get_unused_letters(password: str) -> str:
    """
    Get the letters unused in the password
    :param password: The password
    :return: The letters not used in the password
    """
    alphabet_set = set('abcdefghijklmnopqrstuvwxyz')
    password_set = set(password.lower())
    return ''.join(sorted(alphabet_set - password_set))

def generate_password(state=0, captcha='', location='', chess_move='', link='', color='', unused_letters=''):
    """
    Generates the password for the given state and strings
    :param state: The state of the password (0-5)
    :param captcha: The captcha answer
    :param location: The country name from geoguesser
    :param chess_move: The chess move in algebraic notation
    :param link: The youtube link
    :param color: The hex code of the color
    :return: The password
    """
    match state:
        case 0:
             #data.paul + data.stronk + data.affirmation + data.smol_food +
            password = '101' + 'may' + 'XXXV' + 'sHell' + get_moon_phase()
            return password + sum_25(password)
        case 1:
            password = '101' + 'may' + 'XXXV' + 'sHell' + get_moon_phase() + captcha + get_wordle_answer()
            return password + sum_25(password)
        case 2:
            password = '101' + 'may' + '0' + 'XXXV' + 'sHell' + get_moon_phase() + captcha + get_wordle_answer() + location
            return password + sum_25(password)
        case 3:
            password = data.paul + data.smol_food + data.stronk + '101' + 'may' + '0' + data.affirmations[0] + 'XXXV' + 'shell' + get_moon_phase() + captcha + get_wordle_answer() + location + chess_move
            return password + sum_25(password) + get_element_string(password)
        case 4:
            partial_password = get_wordle_answer() + location + chess_move
            maximized_section = maximize_unused_letters(partial_password, captcha, link)
            password = data.paul + data.smol_food + '0' + data.stronk + get_moon_phase() + '101' + maximized_section + get_wordle_answer() + location + chess_move
            print(digit_sum(password+get_time()))
            return password + sum_25(password) + get_element_string(password), password
        case 5:
            partial_password = get_wordle_answer() + location + chess_move
            maximized_section = maximize_unused_letters(partial_password, captcha, link)
            print(get_unused_letters(maximized_section+location+get_wordle_answer()+chess_move))
            password = data.paul + data.smol_food + '0' + data.stronk + get_moon_phase() + '101' + maximized_section + get_wordle_answer() + get_time() + location + chess_move + color
            return password + sum_25(password) + get_element_string(password, unused_letters)

def password_to_html(state=0, password=''):
    """
    Converts the password to html
    :param state: The state of the password (0-5)
    :param password: The password
    :return: The html string
    """
    match state:
        case 0:
            return "arguments[0].innerHTML = '<p>" + password + "</p>'"
        case 1:
            return "arguments[0].innerHTML = '<p>" + password + "</p>'"
        case 2:
            return "arguments[0].innerHTML = '<p>" + password + "</p>'"
        case 3:
            modified = ""
            for char in password:
                if char in "aeiouyAEIOUY":
                    modified += "<strong>" + char + "</strong>"
                else:
                    modified += "<em>" + char + "</em>"
            return "arguments[0].innerHTML = '<p>" + modified + "</p>'"
        case 4:
            modified = ""
            modified += "<span style=\"font-family: Wingdings; font-size: 28px\">"
            count = 0
            for char in password:
                if char in "aeiouyAEIOUY":
                    modified += "<strong>" + char + "</strong>"
                else:
                    modified += "<em>" + char + "</em>"
                if count == 30:
                    modified += "</span>"
                count += 1
            return "arguments[0].innerHTML = '<p>" + modified + "</p>'"
        case 5:
                default_font = 'Wingdings'
                modified = ""
                used_letters = defaultdict(int)
                count = 0
                for char in password:
                    used_letters[char.lower()] += 1
                    if ord(char) in [65039, 8205, 9794]:
                        size = used_letters['🏋']
                    else:
                        size = used_letters[char.lower()]
                    if char in "IVXLCDM":
                        modified += "<span style=\"font-family: Times New Roman; font-size: " + str(data.font_sizes[size]) + "px\">"
                    else:
                        modified += "<span style=\"font-family: " + default_font + "; font-size: " + (str(int(char)**2) if char.isdigit() else str(data.font_sizes[size])) + "px\">"
                    if char in "aeiouyAEIOUY":
                        modified += "<strong>" + char + "</strong>"
                    else:
                        modified += "<em>" + char + "</em>"
                    modified += "</span>"
                    if count == 30:
                        default_font = 'Monospace'
                    count += 1
                return "arguments[0].innerHTML = '<p>" + modified + "</p>'"
        
def maximize_unused_letters(letters, captcha, link):
    letters_set = set(''.join(x for x in letters.lower() if x.isalpha()))
    captcha_set = set(''.join(x for x in captcha.lower() if x.isalpha()))
    link_set = set(''.join(x for x in link.lower() if x.isalpha()))
    for affirmation in range(len(data.affirmation_sets)):
        for sponsor in range(len(data.sponsors_sets)):
            for month in range(len(data.month_sets)):
                for roman in ['XXXV', 'VIIV']:
                    if len(set('abcdefghijklmnopqrstuvwxyz')-(captcha_set|link_set|letters_set|data.affirmation_sets[affirmation]|data.sponsors_sets[sponsor]|data.month_sets[month]|set(roman.lower()))) >= 2:
                        print(set('abcdefghijklmnopqrstuvwxyz')-(captcha_set|link_set|letters_set|data.affirmation_sets[affirmation]|data.sponsors_sets[sponsor]|data.month_sets[month]|set(roman.lower())))
                        return data.affirmations[affirmation] + data.sponsors[sponsor] + data.months[month] + roman + captcha + link
    print('WEE WOO OMEGA BAD')

def get_moon_phase():
    mi = pylunar.MoonInfo((0,0,0),(0,0,0))
    EASTERN = pytz.timezone('US/Eastern')
    eastern_time = datetime.now(tz=EASTERN)
    datetime_tuple = (eastern_time.year, eastern_time.month, eastern_time.day, 0, 0, 0)
    mi.update(datetime_tuple)
    return data.lunar_dict[mi.phase_name()]