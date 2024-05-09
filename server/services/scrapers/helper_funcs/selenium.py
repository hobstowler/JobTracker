import time

from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from server.services.base import BaseService


def handle_sign_in(service: BaseService):
    if service.source.name == 'indeed':
        return handle_indeed_sign_in(service)

    raise NotImplementedError


def skip_onboarding_steps(service: BaseService):
    if service.source.name == 'indeed':
        return skip_indeed_onboarding_steps(service)

    raise NotImplementedError


def advance_page(service: BaseService):
    if service.source.name == 'indeed':
        return indeed_advance_page(service)

    raise NotImplementedError


def handle_indeed_sign_in(service: BaseService) -> any:
    try:
        sign_in_link = service.driver.find_element(By.XPATH, '//a[text()="Sign in"]')
    except NoSuchElementException:
        print('Couldn\'t find the Sign In element')
        return None

    sign_in_url = sign_in_link.get_attribute('href')
    service.driver.get(sign_in_url)

    # Automatically add email to field and wait for user to continue and potentially resolve Captcha challenge
    email_field = WebDriverWait(service.driver, timeout=60).until(ec.element_to_be_clickable((By.NAME, '__email')))
    if email_field is not False:
        email_field.send_keys(service.options.get('email', ''))

    # Automatically click option to have code sent to email
    fallback_option = WebDriverWait(service.driver, timeout=60).until(
        ec.element_to_be_clickable((By.ID, 'auth-page-google-otp-fallback')))
    if fallback_option is not False:
        fallback_option.click()

    # Wait for user to input code from email
    sign_in_button = WebDriverWait(service.driver, timeout=300).until(
        ec.element_to_be_clickable((
            By.XPATH, '//div[contains(@class, "pass-FormContent")]//button[.//span[text()="Sign in"]]')))
    if sign_in_button is not False:
        sign_in_button.click()
        time.sleep(1)

    service.driver.get(service.source.url)

    # if service.options.get('skip_onboarding', True):
    #     skip_onboarding_steps(service)

    WebDriverWait(service.driver, timeout=500).until(ec.visibility_of_element_located((By.ID, 'text-input-what')))
    time.sleep(1)

    return True


def skip_indeed_onboarding_steps(service: BaseService):
    while ec.url_contains('https://onboarding.indeed.com/'):  # TODO fix magic string :)
        try:
            skip_button = WebDriverWait(service.driver, timeout=5).until(
                ec.element_to_be_clickable((By.XPATH, '//button[./span[text()="Skip"]]')))
            skip_button.click()
        except TimeoutException:
            return
        except ElementClickInterceptedException:
            print('Skip button obscured. Returning...')
            return
        else:
            time.sleep(.1)


def indeed_advance_page(service: BaseService):
    try:
        next_url = service.driver.find_element(By.XPATH, '//a[@aria-label="Next Page"]').get_attribute('href')
        service.driver.get(next_url)
    except NoSuchElementException:
        print('No more pages.')
        return False
    return True
