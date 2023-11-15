# handles selenium webdriver connection and parses data from website
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import data
import solver
import re
from time import sleep

def get_text_box():
    """
    Get the WebElement object to type in
    :return: A WebElement object containing a text box
    """
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProseMirror")))

def set_final_text_box():
    """Changes the text box to the final text box"""
    global box
    box = driver.find_elements(By.CLASS_NAME, "ProseMirror")[-1]

def type_password_html(html: str):
    """Types the password into the text box using javascript"""
    driver.execute_script(html, box)

def get_captcha_answer() -> str:
    """
    Gets the captcha string
    :return: The captcha string
    """
    # explicit wait
    wrapper = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "captcha-wrapper")))
    element = wrapper.find_element(By.CLASS_NAME, "captcha-img")
        # get src image attribute
    answer = element.get_attribute("src").split("/")[-1].split(".")[0]
    # sum of digits in answer
    total = sum([int(num) for num in answer if num.isdigit()])
    refresh = WebDriverWait(wrapper, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "captcha-refresh")))
    while total > 0:
        click_button(refresh)
        answer = element.get_attribute("src").split("/")[-1].split(".")[0]
        total = sum([int(num) for num in answer if num.isdigit()])
    return answer

def get_location() -> str:
    """
    Gets the location from the geoguesser game
    :return: The country name
    """
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "geo-wrapper")))
    # get child of element
    link = element.find_element(By.XPATH, "./child::*").get_attribute("src")
    # search for link in maps.jsonc and return location
    return data.locations[link]

def get_chess_move() -> str:
    """
    Gets the answer to the chess puzzle in algebraic notation
    :return: The answer to the chess puzzle in algebraic notation
    """
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "chess-img")))
    index = element.get_attribute("src").split("puzzle")[-1].split(".")[0]
    return data.moves[int(index)]

def get_video() -> str:
    """
    Gets the video link from the youtube video
    :return: The video link
    """
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "youtube")))
    text = element.get_attribute("innerText")[10:]
    res = [re.sub('[^0-9]','', half) for half in text.split('minute')]
    key = res[0] + ':' + f"{(res[1] if res[1] else '00'):0>2}"
    return 'youtu.be/' + data.videos[key]

def click_unused(unused: str):
    """
    Clicks the letters to sacrifice
    :param unused: The letters to sacrifice (2-letter string)
    """
    print(unused)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sacrafice-area")))
    letters = [letter for letter in element.find_elements(By.CLASS_NAME, "letter") if letter.text.lower() in unused]
    for letter in letters:
        # wait for letter to be clickable
        WebDriverWait(letter, 10).until(EC.element_to_be_clickable(letter))
        click_button(letter)
    click_button(WebDriverWait(element,10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sacrafice-btn"))))

def get_color(old_password: str, unused_letters: str) -> str:
    """
    Gets the hex code of the color shown (will reload the color until an appropriate color is shown)
    :param old_password: The password before the color hex is added
    :param unused_letters: The letters that cannot be in the hex code
    :return: The hex code of the color shown
    """
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
    else:
        sleep(0.1)
    while total > 25 or set(hex_string) & banned_letters:
        click_button(refresh)
        nums = [int(num) for num in element.get_attribute("style").split("(")[-1][0:-2].split(", ")]
        hex_string = '%02x%02x%02x' % tuple(nums)
        print(hex_string)
        cur_time = datetime.now().strftime("%I%M")
        total = sum([int(num) for num in hex_string if num.isdigit()]) + sum_in + sum([int(num) for num in cur_time])
    return '#' + hex_string

def click_final_button():
    """
    Clicks the comfirmation button
    """
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "final-password")))
    button = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
    click_button(button)

def click_button(button):
    """
    Clicks the provided button
    """
    while True:
        try:
            button.click()
        except exceptions.ElementClickInterceptedException:
            pass
        else:
            break

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(options=options)
driver.maximize_window()
driver.get("https://neal.fun/password-game/")

box = get_text_box()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def find_lowest(vertices: list[Point]):
    left = 0
    right = len(vertices)

    mid = (left + right) // 2

    while left < right + 1:
        mid = (left + right) // 2

        left_cmp = vertices[left + 1].y - vertices[left].y
        mid_cmp = vertices[mid + 1].y - vertices[mid].y

        # both decreasing
        if (left_cmp < 0 and mid_cmp < 0):
            if vertices[left].y < vertices[mid].y:
                right = mid
            else:
                left = mid + 1
        # both increasing
        elif (left_cmp > 0 and mid_cmp > 0):
            if vertices[left].y > vertices[mid].y:
                right = mid
            else:
                left = mid + 1
        # only left decreasing
        elif left_cmp < 0:
            right = mid
        # only mid decreasing
        else:
            left = mid + 1

    return mid
