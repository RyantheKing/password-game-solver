# a redesign of the main program. Designed to only implement rules once necessary to increase speed and robustness
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime, timezone
import pylunar
import data
import elements
from collections import defaultdict

# states: 
# 0: pre-captcha
# 1: pre-location
# 2: pre-chess
# 3: pre-fire
# 3: pre-video
# 5: pre-unused
# 6: pre-color
# 7: pre-final

def play_game():
    driver = launch_page()
    password = generate_password(state=0)
    box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProseMirror")))
    
    # initial password to obtain captcha
    driver.execute_script(password_to_html(0, password + sum_25(password)), box)

    # get captcha answer to make geoguesser available
    captcha = get_captcha_answer(driver)
    password = generate_password(state=1, captcha=captcha)
    driver.execute_script(password_to_html(1, password + sum_25(password)), box)

    # get location to make chess available
    location = get_location(driver).lower()
    password = generate_password(state=2, captcha=captcha, location=location)
    driver.execute_script(password_to_html(2, password + sum_25(password)), box)

    # get chess move to make fire available
    chess_move = get_chess_move(driver)
    password = generate_password(state=3, captcha=captcha, location=location, chess_move=chess_move)
    password += sum_25(password) + elements.required_elements_str(200 - elements.password_element_sum(password))
    html_pass = password_to_html(3, password)
    driver.execute_script(html_pass, box)

    # remove fire
    driver.execute_script(html_pass, box)

    # get video to make unused letters available
    link = get_video(driver)
    data.paul = '🐔'
    password = generate_password(state=4, captcha=captcha, location=location, chess_move=chess_move, link=link)
    old_password = password
    password += sum_25(password) + elements.required_elements_str(200 - elements.password_element_sum(password))
    driver.execute_script(password_to_html(4, password), box)

    # click banned letters
    unused = get_unused_letters(password)[-2:]
    click_unused(driver, unused)

    # get color to make final button available
    color = get_color(driver, sum([int(num) for num in old_password if num.isdigit()]), unused)
    password = generate_password(state=5, captcha=captcha, location=location, chess_move=chess_move, link=link, color=color)
    password += sum_25(password) + elements.required_elements_str(200 - elements.password_element_sum(password))
    password += '.'*(101-password_length(password))
    html_pass = password_to_html(5, password)
    driver.execute_script(html_pass, box)

    click_final_button(driver)
    box = driver.find_elements(By.CLASS_NAME, "ProseMirror")[-1]
    driver.execute_script(html_pass, box)

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
        
def get_captcha_answer(driver):
    # explicit wait
    wrapper = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "captcha-wrapper")))
    element = wrapper.find_element(By.CLASS_NAME, "captcha-img")
        # get src image attribute
    answer = element.get_attribute("src").split("/")[-1].split(".")[0]
    # sum of digits in answer
    total = sum([int(num) for num in answer if num.isdigit()])
    refresh = WebDriverWait(wrapper, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "captcha-refresh")))
    while total > 0:
        refresh.click()
        answer = element.get_attribute("src").split("/")[-1].split(".")[0]
        total = sum([int(num) for num in answer if num.isdigit()])

    return answer

def get_wordle_answer():
    # uses requests library
    response = requests.get("https://neal.fun/api/password-game/wordle?date=" + date.today().strftime("%Y-%m-%d"))
    return response.json()['answer']

def get_location(driver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "geo-wrapper")))
    # get child of element
    link = element.find_element(By.XPATH, "./child::*").get_attribute("src")
    # search for link in maps.jsonc and return location
    return data.locations[link]

def get_chess_move(driver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "chess-img")))
    index = element.get_attribute("src").split("puzzle")[-1].split(".")[0]
    return data.moves[int(index)]

def get_video(driver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "youtube")))
    text = element.get_attribute("innerText")
    key = text.split(' minute')[0].split(' ')[-1] + ':' + f"{int(text.split(' second')[0].split(' ')[-1]):02d}"
    return 'youtu.be/' + data.videos[key]

def get_unused_letters(password):
    alphabet_set = set('abcdefghijklmnopqrstuvwxyz')
    password_set = set(password.lower())
    return ''.join(sorted(alphabet_set - password_set))

def click_unused(driver, unused):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sacrafice-area")))
    letters = [letter for letter in element.find_elements(By.CLASS_NAME, "letter") if letter.text.lower() in unused]
    for letter in letters:
        # wait for letter to be clickable
        WebDriverWait(letter, 10).until(EC.element_to_be_clickable(letter))
        letter.click()
    (WebDriverWait(element,10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sacrafice-btn")))).click()

def launch_page():
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(options=options)
    driver.get("https://neal.fun/password-game/")
    return driver

def get_color(driver, sum_in, unused_letters):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rand-color")))
    nums = [int(num) for num in element.get_attribute("style").split("(")[-1][0:-2].split(", ")]
    banned_letters = set(unused_letters)
    # convert rgb (nums) to hex
    hex_string = '%02x%02x%02x' % tuple(nums)
    cur_time = datetime.now().strftime("%I%M")
    total = sum([int(num) for num in hex_string if num.isdigit()]) + sum_in + sum([int(num) for num in cur_time])
    if total > 25 or set(hex_string) & banned_letters:
        refresh = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "refresh")))
    while total > 25 or set(hex_string) & banned_letters:
        refresh.click()
        nums = [int(num) for num in element.get_attribute("style").split("(")[-1][0:-2].split(", ")]
        hex_string = '%02x%02x%02x' % tuple(nums)
        cur_time = datetime.now().strftime("%I%M")
        total = sum([int(num) for num in hex_string if num.isdigit()]) + sum_in + sum([int(num) for num in cur_time])

    return '#' + hex_string

def get_time():
    # gets the time in HH:MM format
    return datetime.now().strftime("%I:%M")

def click_final_button(driver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "final-password")))
    button = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
    button.click()

def password_length(password):
    return len([char for char in password if ord(char) not in [65039, 8205, 9794]])

play_game()