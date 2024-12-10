from urllib import parse

from selenium import webdriver
from selenium.webdriver.common.by import By

from app.core.settings import settings
from app.gonets.http_parse import get_list_messages
from app.gonets.captcha_solver import (
    get_captcha_as_base64_or_none,
    solve_captcha,
)


COOKIE_USER_LOGIN: str = "userLoginGS"


def create_webdriver(
    remote_url: str = None,
    options: list | None = None,
) -> webdriver.Chrome:
    if not options:
        options = ["--headless"]

    driver_options = webdriver.ChromeOptions()
    [driver_options.add_argument(option) for option in options]

    if remote_url:
        driver = webdriver.Remote(
            command_executor=remote_url,
            options=driver_options,
        )
    else:
        driver = webdriver.Chrome(
            options=driver_options,
        )

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


def get_cookies_http_format(
    driver: webdriver.Chrome,
) -> dict:
    def set_cookie(cookies, cookie):
        cookies.setdefault(
            cookie.get("name"),
            parse.quote(cookie.get("value")),
        )

    cookies = {}
    [set_cookie(cookies, cookie) for cookie in driver.get_cookies()]

    return cookies


def get_user_id_from_cookies(cookies):
    return cookies.get(COOKIE_USER_LOGIN)


def get_gonets_info(remote_url: str | None = None):
    if remote_url:
        driver = create_webdriver(remote_url)
    else:
        driver = create_webdriver()

    with driver:
        driver.get(settings.GONETS.BASE_URL + settings.GONETS.LOGIN_ROUTE)

        if not (encoded_captcha := get_captcha_as_base64_or_none(driver)):
            print("Captcha not found, go to main page")

        result = solve_captcha(encoded_captcha)
        fill_form_and_enter(driver, result)

        selenuim_cookies = get_cookies_http_format(driver)
        user_id = get_user_id_from_cookies(selenuim_cookies)

    messages = get_list_messages(selenuim_cookies, user_id)

    return messages
