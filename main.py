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

def play_game():
    driver = launch_page()
    password = generate_password()
    box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProseMirror")))

    driver.execute_script(password_to_html(password), box)

    captcha = get_captcha_answer(driver)
    password = generate_password(captcha)
    driver.execute_script(password_to_html(password), box)

    location = get_location(driver).lower()
    password = generate_password(captcha, location)
    driver.execute_script(password_to_html(password), box)

    chess_move = get_chess_move(driver)
    password = generate_password(captcha, location, chess_move)
    driver.execute_script(password_to_html(password), box)

    # remove fire
    driver.execute_script(password_to_html(password), box)

    link = get_video(driver)
    data.paul = '🐔'
    password = generate_password(captcha, location, chess_move, link)
    driver.execute_script(password_to_html(password), box)

    unused = get_unused_letters(password)[-2:]
    click_unused(driver, unused)
        
    color = get_color(driver)
    password = generate_password(captcha, location, chess_move, link, color)
    driver.execute_script(password_to_html(password), box)

    click_final_button(driver)

    box = driver.find_elements(By.CLASS_NAME, "ProseMirror")[-1]
    driver.execute_script(password_to_html(password), box)

def password_to_html(password):
    # bold every vowel in password, italicize every non-vowel, all non-alphanumberic
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
        elif char.isdigit():
            modified += "<span style=\"font-family: Monospace; font-size: " + str(int(char)**2) + "px\">"
        else:
            modified += "<span style=\"font-family: Wingdings; font-size: " + str(data.font_sizes[size]) + "px\">"
        if char in "aeiouyAEIOUY":
            modified += "<strong>" + char + "</strong>"
        else:
            modified += "<em>" + char + "</em>"
        modified += "</span>"
        count += 1

    return "arguments[0].innerHTML = '<p>" + modified + "</p>'"

def generate_password(captcha='', location='', chess_move='', link='', color=''):
    # 5: digits must add to 25
    # 6: needs to include a month
    # 8: needs to include a sponsor
    # 9: needs to multiply to 35
    # 10: captcha
    sponsor = 'sHell'  # somewhat mandatory
    month = 'may'  # somewhat mandatory
    thiry_five_mult = 'XXXV'  # mandatory
    wordle = get_wordle_answer()  # mandatory
    cur_time = get_time()  # mandatory
    moon = '🌑🌒🌓🌔🌕🌖🌗🌘' # mandatory
    leap_year = '0'  # mandatory
    atomic_number_requirement = 200

    # numbers:
    # 1: current time (min: 0, max: 24 (19:59))
    # 2: catpcha (avoidable)
    # 3: chess move (min: 1, max: 8)
    # 4: youtube link (potentially avoidable but very difficult)
    # 5: color (avoidable)
    # 6: password length (prime number) (min: 2, max: 17)

    updated_password = data.paul + data.stronk + data.affirmation + data.food + leap_year + sponsor + month + thiry_five_mult + wordle + cur_time + moon + captcha + location \
                       + chess_move + link + color
    updated_password += elements.required_elements_str(atomic_number_requirement - elements.password_element_sum(updated_password))

    length = password_length(updated_password)+3
    # round length up to the nearest prime in data.primes
    for prime in data.primes:
        if prime >= length and int(sum_25(updated_password+str(prime))) >= 0:
            length = prime
            break
    updated_password += str(length)
    sum = sum_25(updated_password)
    updated_password += sum
    num_dots = length - password_length(updated_password)
    for i in range((num_dots-1)//14+1):
        updated_password += data.chars[i]*(num_dots-i*14 if num_dots//14 == i else 14)
    # updated_password += '@'*(num_dots//2) + '.'*(num_dots-num_dots//2)
    # previous_attempt = updated_password
    # updated_password = old_password
    # while True:
    #     length = password_length(updated_password)
    #     updated_password += str(length + len(str(length)))
    #     updated_password += sum_25(updated_password)
    #     print(updated_password[-6:])
    #     if updated_password == previous_attempt:
    #         break
    #     previous_attempt = updated_password
    #     updated_password = old_password

    return updated_password


def launch_page():
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(options=options)
    driver.get("https://neal.fun/password-game/")
    return driver


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

def password_length(password):
    return len([char for char in password if ord(char) not in [65039, 8205, 9794]])

def get_wordle_answer():
    # uses requests library
    response = requests.get("https://neal.fun/api/password-game/wordle?date=" + date.today().strftime("%Y-%m-%d"))
    return response.json()['answer']


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


def get_moon_phase():
    # uses pylunar library
    mi = pylunar.MoonInfo((0, 0, 0), (0, 0, 0))
    # use UTC
    utc = datetime.now(timezone.utc)
    datetime_tuple = (utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second)
    mi.update(datetime_tuple)
    return data.lunar_dict[mi.phase_name()]


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
    letters = element.find_elements(By.CLASS_NAME, "letter")
    for letter in letters:
        if letter.text.lower() in unused:
            letter.click()
    element.find_element(By.CLASS_NAME, "sacrafice-btn").click()

def get_color(driver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rand-color")))
    nums = [int(num) for num in element.get_attribute("style").split("(")[-1][0:-2].split(", ")]
    # convert rgb (nums) to hex
    hex_string = '#%02x%02x%02x' % tuple(nums)
    total = sum([int(num) for num in hex_string if num.isdigit()])
    refresh = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "refresh")))
    while total > 0:
        refresh.click()
        nums = [int(num) for num in element.get_attribute("style").split("(")[-1][0:-2].split(", ")]
        hex_string = '#%02x%02x%02x' % tuple(nums)
        total = sum([int(num) for num in hex_string if num.isdigit()])

    return hex_string

def get_time():
    # gets the time in HH:MM format
    return datetime.now().strftime("%I:%M")

def click_final_button(driver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "final-password")))
    yes = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.XPATH, "./child::*")))
    yes.click()

play_game()
