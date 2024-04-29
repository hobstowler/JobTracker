import time
from typing import Optional

import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from sqlalchemy.exc import NoResultFound

from server.models import Job, Company
from server.repositories import CompanyRepository, JobRepository, SourceRepository


class IndeedScrapingService:
    job_repository = JobRepository
    company_repository = CompanyRepository()
    source_repository = SourceRepository()

    def __init__(self, num_pages=1, **kwargs):
        self.source = self.source_repository.get_by_name('indeed')
        if self.source:
            self._start_url = self.source.url
        else:
            raise NoResultFound()

        self._options = {
            'num_pages': num_pages
        }
        self._options.update(kwargs)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

        self.job_repository = self.job_repository()

    def scrape(self):
        num_pages = self._options.get('num_pages')

        self.driver.get(self._start_url)
        time.sleep(1)

        if self.handle_indeed_sign_in():
            self.perform_search()
        else:
            raise Exception("Could not sign in")

        for i in range(num_pages):
            print(f'Page {i + 1}')
            job_cards = self.driver.find_elements(
                By.XPATH, '//div[@id="mosaic-provider-jobcards"]/ul/li[./div[contains(@class, "cardOutline")]]')

            for job in job_cards:

                job_title = self._extract_job_title(job)
                company_name, job_location = self._extract_company_and_location(job)
                job_url = self.extract_job_url(job)

                if job_url is None or job_title is None:
                    continue

                company = self.company_repository.get_by_name(company_name)
                if company is None:
                    company = Company()
                    company.name = company_name
                    self.company_repository.add(company)

                new_job = Job(job_title, job_url)
                new_job.company = company
                new_job.source = self.source

            time.sleep(1)

            if i + 1 != num_pages and not self.advance_page():
                break

    def _extract_job_title(self, job) -> Optional[str]:
        job_title_element = job.find_elements(By.CLASS_NAME, 'jcs-JobTitle')
        job_title_element = job_title_element[0] if len(job_title_element) > 0 else None

        if job_title_element is None:
            return

        return job_title_element.find_element(By.TAG_NAME, 'span').text

    def _extract_company_and_location(self, job) -> (Optional[str], Optional[str]):
        company_location = job.find_element(By.CLASS_NAME, 'company_location')

        company = company_location.find_elements(By.XPATH, './/*[contains(@data-testid, "company-name")]')
        # print(f'\t{company[0].text}') if len(company) > 0 else print('\tCompany not detected')
        company = company[0].text if len(company) > 0 else None

        location = company_location.find_elements(By.XPATH, './/*[contains(@data-testid, "text-location")]')
        # print(f'\t{location[0].text}') if len(location) > 0 else print('\tLocation not detected')
        location = location[0].text if len(location) > 0 else None

        return company, location

    def advance_page(self):
        try:
            next_url = self.driver.find_element(By.XPATH, '//a[@aria-label="Next Page"]').get_attribute('href')
            self.driver.get(next_url)
        except NoSuchElementException:
            print('No more pages.')
            return False
        return True

    def extract_job_url(self, job) -> Optional[str]:
        url = None
        easy_apply = False
        if self.check_for_easy_apply(job):
            # print('found, skipping.')
            url = job.find_element(
                By.XPATH, './/a[contains(@class, "jcs-JobTitle")]').get_attribute('href')
            easy_apply = True
        else:
            # print('not found, saving job.')
            job.click()
            time.sleep(.5)

            try:
                apply_button = WebDriverWait(self.driver, timeout=5).until(
                    ec.element_to_be_clickable(
                        (By.XPATH,
                         '//div[@id="jobsearch-ViewjobPaneWrapper"]//button[.//span[text()="Apply now"]]')
                    ))
                if apply_button is not False:
                    apply_button.click()
                else:
                    return None
            except TimeoutException:
                print('\tTimed out waiting for Apply button')

        return self._extract_url_from_new_tab(url, easy_apply)

    def handle_indeed_sign_in(self) -> any:
        try:
            sign_in_link = self.driver.find_element(By.XPATH, '//a[text()="Sign in"]')
        except NoSuchElementException:
            print('couldn\'t find the Sign In element')
            return None

        sign_in_url = sign_in_link.get_attribute('href')
        self.driver.get(sign_in_url)

        # Automatically add email to field and wait for user to continue and potentially resolve Captcha challenge
        email_field = WebDriverWait(self.driver, timeout=60).until(ec.element_to_be_clickable((By.NAME, '__email')))
        if email_field is not False:
            email_field.send_keys(self._options.get('email', ''))

        # Automatically click option to have code sent to email
        fallback_option = WebDriverWait(self.driver, timeout=60).until(
            ec.element_to_be_clickable((By.ID, 'auth-page-google-otp-fallback')))
        if fallback_option is not False:
            fallback_option.click()

        # Wait for user to input code from email
        sign_in_button = WebDriverWait(self.driver, timeout=300).until(
            ec.element_to_be_clickable((
                By.XPATH, '//div[contains(@class, "pass-FormContent")]//button[.//span[text()="Sign in"]]')))
        if sign_in_button is not False:
            sign_in_button.click()
            time.sleep(1)

        self._skip_onboarding_steps()

        WebDriverWait(self.driver, timeout=500).until(ec.visibility_of_element_located((By.ID, 'text-input-what')))
        time.sleep(1)

        return True

    def _skip_onboarding_steps(self):
        while ec.url_contains('https://onboarding.indeed.com/'):
            try:
                skip_button = WebDriverWait(self.driver, timeout=5).until(
                    ec.element_to_be_clickable((By.XPATH, '//button[./span[text()="Skip"]]')))
                skip_button.click()
            except TimeoutException:
                return
            except ElementClickInterceptedException:
                print('Skip button obscured. Returning...')
                return
            else:
                time.sleep(.1)

    def perform_search(self) -> None:
        try:
            title_field = self.driver.find_element(By.ID, 'text-input-what')
            location_field = self.driver.find_element(By.ID, 'text-input-where')
        except NoSuchElementException:
            print('Error locating search elements')
            exit(0)
        else:
            title_field.clear()
            title_field.send_keys(self._options.get('title', ''))

            location_field.clear()
            location_field.send_keys(self._options.get('location', ''))

            location_field.submit()

        time.sleep(2)
        self._select_date_posted_filter()
        self._select_remote_filter()

    def check_for_easy_apply(self, job: selenium.webdriver.remote.webelement.WebElement) -> bool:
        try:
            # print('\tChecking for Easily Apply...', end=' ')
            job.find_element(By.XPATH, './/span[text()="Easily apply"]')
        except NoSuchElementException:
            return False

        return True

    def _select_date_posted_filter(self):
        date_filter_url = self.driver.find_element(
            By.XPATH, '//*[@id="filter-dateposted-menu"]/li/a[text()="Last 24 hours"]').get_attribute('href')
        self.driver.get(date_filter_url)
        time.sleep(1)

    def _select_remote_filter(self):
        remote_filter_url = self.driver.find_element(
            By.XPATH, '//*[@id="filter-remotejob-menu"]/li/a[contains(text(), "Remote")]').get_attribute('href')
        self.driver.get(remote_filter_url)
        time.sleep(1)

    def _extract_url_from_new_tab(self, url=None, easy_apply=False) -> Optional[str]:
        original_window = self.driver.current_window_handle
        job_url = None

        if url is not None:
            self.driver.switch_to.new_window('tab')
            self.driver.get(url)
        else:
            self.driver.switch_to.window(self.driver.window_handles[1])

        try:
            WebDriverWait(self.driver, timeout=5).until(lambda x: self._check_valid_job_url(self.driver.current_url, easy_apply))
        except TimeoutException:
            print('Timed out waiting for page to load.')
        else:
            job_url = self.driver.current_url
        finally:
            time.sleep(1)
            self.driver.close()
            self.driver.switch_to.window(original_window)

            return job_url

    def _check_valid_job_url(self, current_url, easy_apply):
        if current_url == 'about:blank':
            return False
        else:
            if easy_apply:
                return current_url.find('https://www.indeed.com') != -1
            else:
                return current_url.find('https://www.indeed.com') == -1


def main():
    scraper = IndeedScrapingService(
        'https://www.indeed.com',
        num_pages=2,
        title='Software Engineer',
        location='United States',
        email='jameshtowler@gmail.com')
    scraper.scrape()


if __name__ == '__main__':
    main()
