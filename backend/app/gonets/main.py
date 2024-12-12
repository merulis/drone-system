from urllib import parse

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

from app.core.settings import settings
from app.gonets.http_parse import get_list_messages
from app.gonets.captcha_solver import (
    get_captcha_as_base64_or_none,
    solve_captcha,
)
from app.gonets.models import GonetsCookies


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


def format_cookies_to_model(
    cookies_in: list,
) -> GonetsCookies:
    def set_cookie(cookies, cookie):
        cookies.setdefault(
            cookie.get("name"),
            parse.quote(cookie.get("value")),
        )

    cookies_dict = {}
    [set_cookie(cookies_dict, cookie) for cookie in cookies_in]

    cookies = GonetsCookies.model_from_dict(cookies_dict)

    return cookies


def get_gonets_info(
    remote_url: str | None = None,
    date_from: datetime | None = None,
    date_to: None = None,
):
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

        selenium_cookies = driver.get_cookies()
        cookies = format_cookies_to_model(selenium_cookies)
        uid = cookies.login

    messages = get_list_messages(
        cookies=cookies.model_dump(),
        uid=uid,
        date_from=date_from,
        date_to=date_to,
    )

    return messages
