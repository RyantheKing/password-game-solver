import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime, timezone
import pylunar
import data
import time

def play_game():
    driver = launch_page()
    password = generate_password()
    box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProseMirror")))
    driver.execute_script("arguments[0].innerHTML = '<p><span style=\"font-family: Monospace; font-size: 28px\">"+ password +"</span></p>'", box)

    captcha = get_captcha_answer(driver)
    password = generate_password(captcha)
    driver.execute_script("arguments[0].innerHTML = '<p><span style=\"font-family: Monospace; font-size: 28px\">"+ password +"</span></p>'", box)

    location = get_location(driver).lower()
    password = generate_password(captcha, location)
    driver.execute_script("arguments[0].innerHTML = '<p><span style=\"font-family: Monospace; font-size: 28px\">"+ password +"</span></p>'", box)

    chess_move = get_chess_move(driver)
    password = generate_password(captcha, location, chess_move)
    driver.execute_script("arguments[0].innerHTML = '<p><span style=\"font-family: Monospace; font-size: 28px\">"+ password +"</span></p>'", box)

def generate_password(captcha='', location='', chess_move=''):
    # 5: digits must add to 25
    # 6: needs to include a month
    # 8: needs to include a sponsor
    # 9: needs to multiply to 35
    # 10: captcha
    sponsor = 'sHell' # somewhat mandatory
    month = 'may' # somewhat mandatory
    thiry_five_mult = 'XXXV' # mandatory
    wordle = get_wordle_answer() # mandatory
    moon = get_moon_phase() # mandatory
    leap_year = '0'  # mandatory

    updated_password = data.paul + sponsor + month + thiry_five_mult + wordle + moon + leap_year + captcha + location + chess_move
    sum = sum_25(updated_password)

    return data.paul + sponsor + month + thiry_five_mult + wordle + moon + leap_year + captcha + location + chess_move + sum

def launch_page():
    driver = webdriver.Firefox()
    driver.get("https://neal.fun/password-game/")
    return driver

def sum_25(password):
    # sum all the digits in the string and return the difference from 25
    sum = 0
    for char in password:
        if char.isdigit():
            sum += int(char)
    diff = 25 - sum
    return_str = ""
    while diff > 9:
        return_str += "9"
        diff -= 9
    return_str += str(diff)
    return return_str

def get_wordle_answer():
    # uses requests library
    response = requests.get("https://neal.fun/api/password-game/wordle?date="+date.today().strftime("%Y-%m-%d"))
    return response.json()['answer']

def get_captcha_answer(driver):
    # explicit wait
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "captcha-img")))
    # get src image attribute
    return element.get_attribute("src").split("/")[-1].split(".")[0]

def get_moon_phase():
    # uses pylunar library
    mi = pylunar.MoonInfo((0,0,0),(0,0,0))
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

play_game()