# handles selenium webdriver connection and parses data from website
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
import solver
import re

def get_text_box():
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProseMirror")))

def set_final_text_box():
    global box
    box = driver.find_elements(By.CLASS_NAME, "ProseMirror")[-1]

def type_password_html(html):
    driver.execute_script(html, box)

def get_captcha_answer():
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

def get_location():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "geo-wrapper")))
    # get child of element
    link = element.find_element(By.XPATH, "./child::*").get_attribute("src")
    # search for link in maps.jsonc and return location
    return data.locations[link]

def get_chess_move():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "chess-img")))
    index = element.get_attribute("src").split("puzzle")[-1].split(".")[0]
    return data.moves[int(index)]

def get_video():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "youtube")))
    text = element.get_attribute("innerText")[10:]
    res = [re.sub('[^0-9]','', half) for half in text.split('minute')]
    key = res[0] + ':' + f"{(res[1] if res[1] else '00'):02s}"
    return 'youtu.be/' + data.videos[key]

def click_unused(unused):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sacrafice-area")))
    letters = [letter for letter in element.find_elements(By.CLASS_NAME, "letter") if letter.text.lower() in unused]
    for letter in letters:
        # wait for letter to be clickable
        WebDriverWait(letter, 10).until(EC.element_to_be_clickable(letter))
        letter.click()
    WebDriverWait(element,10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sacrafice-btn"))).click()

def get_color(old_password, unused_letters):
    sum_in = solver.digit_sum(old_password)
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

def click_final_button():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "final-password")))
    button = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
    button.click()

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(options=options)
driver.maximize_window()
driver.get("https://neal.fun/password-game/")

box = get_text_box()