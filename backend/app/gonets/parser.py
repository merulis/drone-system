from selenium import webdriver
from selenium.webdriver.common.by import By

from app.core.settings import settings
from app.gonets.arequests import get_messages
from app.gonets.captcha_solver import (
    get_captcha_as_base64_or_none,
    solve_captcha,
)


def create_webdriver(
    options: list | None = None,
) -> webdriver.Chrome:
    if not options:
        options = ["--headless"]

    driver_options = webdriver.ChromeOptions()
    [driver_options.add_argument(option) for option in options]

    driver = webdriver.Chrome(options=driver_options)

    return driver


def fill_form_and_enter(driver: webdriver.Chrome, result):
    login_input = driver.find_element(By.ID, "TextBox_Login")
    password_input = driver.find_element(By.ID, "pass")
    capthca_input = driver.find_element(By.ID, "Captcha")
    enter_button = driver.find_element(By.ID, "Btn_Login")

    login_input.send_keys(settings.GONETS.LOGIN)
    password_input.send_keys(settings.GONETS.PASSWORD)
    capthca_input.send_keys(result.get("code"))

    enter_button.click()


def get_cookies_aiohttp_format(
    driver: webdriver.Chrome,
) -> dict:
    def set_cookie(cookies, cookie):
        cookies.setdefault(cookie.get("name"), cookie.get("value"))

    cookies = {}
    [set_cookie(cookies, cookie) for cookie in driver.get_cookies()]

    return cookies


def get_user_id_from_cookies(cookies):
    return cookies.get(settings.GONETS.COOKIE_USER_LOGIN)


async def parse_message():
    with create_webdriver() as driver:
        driver.get(settings.GONETS.BASE_URL + settings.GONETS.LOGIN_ROUTE)

        if not (encoded_captcha := get_captcha_as_base64_or_none(driver)):
            print("Captcha not found, go to main page")

        result = solve_captcha(encoded_captcha)
        fill_form_and_enter(driver, result)

        selenuim_cookies = get_cookies_aiohttp_format(driver)
        user_id = get_user_id_from_cookies(selenuim_cookies)

    status, json = await get_messages(selenuim_cookies, user_id)

    return status, json
