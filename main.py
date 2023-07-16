import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime, timezone
import pylunar
import data

def generate_password():
    # code for generating string goes here

    return

def launch_page():
    driver = webdriver.Firefox()
    driver.get("https://neal.fun/password-game/")
    return driver


def get_wordle_answer():
    # uses requests library
    response = requests.get("https://neal.fun/api/password-game/wordle?date="+date.today().strftime("%Y-%m-%d"))
    return response.json()['answer']

def get_captcha_answer(driver):
    # enter text
    box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProseMirror")))
    box.send_keys("march997@pepsiVIIV")
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
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "geo")))
    link = element.get_attribute("src")
    # search for link in maps.jsonc and return location
    return data.locations[link]

def get_chess_move(driver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "chess-img")))
    index = element.get_attribute("src").split("puzzle")[-1].split(".")[0]
    return data.moves[int(index)]

get_chess_move()