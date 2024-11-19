import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By

from twocaptcha import TwoCaptcha

from aiohttp import ClientSession

from app.core.settings import settings


def create_webdriver(
    options: list | None = None,
) -> webdriver.Chrome:
    if not options:
        options = ["--headless"]

    driver_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=driver_options)

    [driver_options.add_argument(option) for option in options]

    return driver


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


def fill_form_and_enter(driver: webdriver.Chrome, result):
    login_input = driver.find_element(By.ID, "TextBox_Login")
    password_input = driver.find_element(By.ID, "pass")
    capthca_input = driver.find_element(By.ID, "Captcha")
    enter_button = driver.find_element(By.ID, "Btn_Login")

    login_input.send_keys(settings.GONETS.LOGIN)
    password_input.send_keys(settings.GONETS.PASSWORD)
    capthca_input.send_keys(result.get("code"))

    enter_button.click()


def get_cookies_for_aiohttp(
    driver: webdriver.Chrome,
) -> dict:
    def set_cookie(cookies, cookie):
        cookies.setdefault(cookie.get("name"), cookie.get("value"))

    cookies = {}
    [set_cookie(cookies, cookie) for cookie in driver.get_cookies()]

    return cookies


def get_user_id_from_cookies(cookies):
    return cookies.get(settings.GONETS.COOKIE_USER_LOGIN)


async def get_messages(selenuim_cookies, user_id):
    async with ClientSession(cookies=selenuim_cookies) as session:
        url = settings.GONETS.BASE_URL + settings.GONETS.LIST_MESSAGE_ROUTE

        json = settings.GONETS.LIST_MESSAGE_JSON
        json[settings.GONETS.LIST_MESSAGE_USER_ID] = user_id

        async with session.post(
            url=url,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json; charset=utf-8,",
            },
            json=json,
        ) as response:
            status = response.status
            message_json = await response.json()

        return status, message_json


async def main():
    driver = create_webdriver()

    driver.get(settings.GONETS.BASE_URL + settings.GONETS.LOGIN_ROUTE)

    if not (encoded_captcha := get_captcha_as_base64_or_none(driver)):
        print("Captcha not found, go to main page")

    result = solve_captcha(encoded_captcha)
    fill_form_and_enter(driver, result)

    selenuim_cookies = get_cookies_for_aiohttp(driver)
    user_id = get_user_id_from_cookies(selenuim_cookies)

    driver.quit()

    status, json = await get_messages(selenuim_cookies, user_id)
    print(status, json)


asyncio.run(main())
