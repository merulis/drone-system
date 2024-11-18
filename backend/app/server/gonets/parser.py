from selenium import webdriver
from selenium.webdriver.common.by import By

from twocaptcha import TwoCaptcha

import time
import uuid
import base64

from app.core.settings import settings


def solve_captcha(encoded_data):
    solver = TwoCaptcha(apiKey=settings.CAPTCHA.API_KEY)

    try:
        result = solver.normal(encoded_data)
    except Exception as e:
        raise e
    else:
        return result


def get_captcha_path_or_none(driver: webdriver.Chrome):
    try:
        captcha = driver.find_element(By.ID, "CaptchaI")

    except Exception:
        return None

    image_name = f"{str(uuid.uuid4())}.png"
    image_path = settings.CAPTCHA.IMG_FOLDER / image_name
    _ = captcha.screenshot(str(image_path))

    return image_path


def encode_captcha_img_bs64(image_path):
    if not image_path.exists():
        time.sleep(0.3)

    with open(image_path, "rb") as file:
        data = file.read()

    encoded_data = base64.b64encode(data).decode("utf-8")
    return encoded_data


def fill_form_and_enter(driver, result):
    login_input = driver.find_element(By.ID, "TextBox_Login")
    password_input = driver.find_element(By.ID, "pass")
    capthca_input = driver.find_element(By.ID, "Captcha")
    enter_button = driver.find_element(By.ID, "Btn_Login")

    login_input.send_keys(settings.GONETS.LOGIN)
    password_input.send_keys(settings.GONETS.PASSWORD)
    capthca_input.send_keys(result.get("code"))

    enter_button.click()


def main():
    driver = webdriver.Chrome()
    driver.get(settings.GONETS.BASE_URL + settings.GONETS.LOGIN_URL)

    image_path = get_captcha_path_or_none(driver)

    if not image_path:
        print("Captcha not found, go to main page")

    encoded_captcha = encode_captcha_img_bs64(image_path)
    result = solve_captcha(encoded_captcha)
    fill_form_and_enter(driver, result)

    driver.quit()


main()
