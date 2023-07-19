# generates password and make a few other calculations like the total sum for digits and elements
import data
import elements
import requests
from datetime import datetime
from collections import defaultdict

def birth_paul():
    data.paul = '🐔'

def digit_sum(password : str) -> int:
    return sum([int(num) for num in password if num.isdigit()])

def get_wordle_answer():
    # uses requests library
    response = requests.get("https://neal.fun/api/password-game/wordle?date=" + datetime.today().strftime("%Y-%m-%d"))
    return response.json()['answer']

def get_time():
    # gets the time in HH:MM format
    return datetime.now().strftime("%I:%M")

def sum_25(password):
    # sum all the digits in the string and return the difference from 25
    le_sum = 0
    for char in password:
        if char.isdigit():
            le_sum += int(char)
    diff = 25 - le_sum
    return_str = ""
    while diff > 9:
        return_str += "9"
        diff -= 9
    return_str += str(diff)
    return return_str

def get_element_string(password):
    return elements.required_elements_str(200 - elements.password_element_sum(password))

def dot_string(password):
    return '.'*(101-password_length(password))

def password_length(password):
    return len([char for char in password if ord(char) not in [65039, 8205, 9794]])

def get_unused_letters(password):
    alphabet_set = set('abcdefghijklmnopqrstuvwxyz')
    password_set = set(password.lower())
    return ''.join(sorted(alphabet_set - password_set))

def generate_password(state=0, captcha='', location='', chess_move='', link='', color=''):
    # generate password based on current state
    match state:
        case 0:
             #data.paul + data.stronk + data.affirmation + data.smol_food +
            return '101' + 'may' + 'XXXV' + 'sHell' + '🌑🌒🌓🌔🌕🌖🌗🌘'
        case 1:
            return '101' + 'may' + 'XXXV' + 'sHell' + '🌑🌒🌓🌔🌕🌖🌗🌘' + captcha + get_wordle_answer()
        case 2:
            return '101' + 'may' + '0' + 'XXXV' + 'sHell' + '🌑🌒🌓🌔🌕🌖🌗🌘' + captcha + get_wordle_answer() + location
        case 3:
            return data.paul + data.smol_food + data.stronk + '101' + 'may' + '0' + data.affirmation + 'XXXV' + 'shell' + '🌑🌒🌓🌔🌕🌖🌗🌘' + captcha + get_wordle_answer() + location + chess_move
        case 4:
            return data.paul + data.smol_food + data.stronk + data.affirmation + '🌑🌒🌓🌔🌕🌖🌗🌘' + '101' + 'may' + 'shell' + '0' + 'XXXV' + captcha + get_wordle_answer() + location + chess_move + link
        case 5:
            return data.paul + data.smol_food + data.stronk + data.affirmation + '🌑🌒🌓🌔🌕🌖🌗🌘' + '101' + 'may' + 'shell' + '0' + 'XXXV' + captcha + get_wordle_answer() + get_time() + location + chess_move + link + color
        
def password_to_html(state=0, password=''):
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
            for char in password:
                if char in "aeiouyAEIOUY":
                    modified += "<strong>" + char + "</strong>"
                else:
                    modified += "<em>" + char + "</em>"
                if char == '🌘':
                    modified += "</span>"
            return "arguments[0].innerHTML = '<p>" + modified + "</p>'"
        case 5:
                default_font = 'Wingdings'
                modified = ""
                used_letters = defaultdict(int)
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
                    if char == '🌘':
                        default_font = 'Monospace'
                return "arguments[0].innerHTML = '<p>" + modified + "</p>'"