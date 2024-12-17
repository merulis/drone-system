from app.core.settings import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha


def get_captcha_as_base64_or_none(driver: webdriver.Chrome):
    try:
        captcha = driver.find_element(By.ID, "CaptchaI")

    except Exception:
        return None

    captcha_base64 = captcha.screenshot_as_base64

    return captcha_base64


def solve_captcha(encoded_data):
    solver = TwoCaptcha(apiKey=settings.CAPTCHA.API_KEY)

    try:
        result = solver.normal(encoded_data)
    except Exception as e:
        raise e
    else:
        return result
