import time
from typing import Optional
from urllib.parse import urlparse

import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from server.models import Job, Company, Source, User, Search
from server.repositories import CompanyRepository, JobRepository
from server.services.base import BaseService
from server.services.scrapers.helper_funcs.selenium import handle_sign_in, advance_page

APPLY_BUTTON_TIMEOUT = '\tTimed out waiting for Apply button'
APPLY_NOW_BUTTON = '//div[@id="jobsearch-ViewjobPaneWrapper"]//button[.//span[text()="Apply now"]]'
COMPANY_LOCATION_XPATH = './/*[contains(@data-testid, "text-location")]'
COMPANY_NAME_XPATH = './/*[contains(@data-testid, "company-name")]'
EASY_APPLY_URL = './/a[contains(@class, "jcs-JobTitle")]'
JOB_TITLE_ELEMENT = 'jcs-JobTitle'
JOB_CARDS = '//div[@id="mosaic-provider-jobcards"]/ul/li[./div[contains(@class, "cardOutline")]]'
LAST_24_HOURS_XPATH = '//*[@id="filter-dateposted-menu"]/li/a[text()="Last 24 hours"]'
PAGE_LOAD_TIMEOUT = 'Timed out waiting for page to load.'
REMOTE_XPATH = '//*[@id="filter-remotejob-menu"]/li/a[contains(text(), "Remote")]'


class IndeedScrapingService(BaseService):
    job_repository = JobRepository()
    company_repository = CompanyRepository()

    def __init__(self, user: User, source: Source, search: Search, options: dict = None):
        self.user = user
        self.source = source
        self.search = search

        if not options:
            self.options = {
                'skip_onboarding': True
            }
        self.options.update({
            'num_pages': self.options['num_pages'] if self.options.get('num_pages') else 1
        })

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

    def scrape(self):
        num_pages = self.options.get('num_pages')

        self.driver.get(self.source.url)
        time.sleep(1)

        if handle_sign_in(self):
            self.perform_search()
        else:
            raise Exception("Could not sign in")

        for i in range(num_pages):
            print(f'Page {i + 1}')
            WebDriverWait(self.driver, timeout=10).until(ec.visibility_of_element_located((
                By.XPATH, JOB_CARDS
            )))
            job_cards = self.driver.find_elements(
                By.XPATH, JOB_CARDS)

            for job in job_cards:

                job_title = self._extract_job_title(job)
                print('\t', job_title)
                company_name, job_location = self._extract_company_and_location(job)
                job_url = self.extract_job_url(job)
                print('\t', job_url)

                if job_url is None or job_title is None:
                    continue

                company = self.company_repository.get_by_name(company_name)
                if company is None:
                    company = Company(company_name)
                    self.company_repository.add(company)

                new_job = self.job_repository.get_by_url(job_url)
                if new_job:
                    new_job.update_date_added()
                    self.job_repository.update(new_job)
                else:
                    new_job = Job(job_title, job_url)
                    new_job.company = company
                    new_job.source = self.source
                    self.job_repository.add(new_job)

                # self.user_repository.add_job_to_user(self.user, new_job)

            time.sleep(1)

            if i + 1 != num_pages and not advance_page(self):
                break

    def _extract_job_title(self, job) -> Optional[str]:
        job_title_element = job.find_elements(By.CLASS_NAME, JOB_TITLE_ELEMENT)
        job_title_element = job_title_element[0] if len(job_title_element) > 0 else None

        if job_title_element is None:
            return

        return job_title_element.find_element(By.TAG_NAME, 'span').text

    def _extract_company_and_location(self, job) -> (Optional[str], Optional[str]):
        company_location = job.find_element(By.CLASS_NAME, 'company_location')

        company = company_location.find_elements(By.XPATH, COMPANY_NAME_XPATH)
        # print(f'\t{company[0].text}') if len(company) > 0 else print('\tCompany not detected')
        company = company[0].text if len(company) > 0 else None

        location = company_location.find_elements(By.XPATH, COMPANY_LOCATION_XPATH)
        # print(f'\t{location[0].text}') if len(location) > 0 else print('\tLocation not detected')
        location = location[0].text if len(location) > 0 else None

        return company, location

    def extract_job_url(self, job) -> Optional[str]:
        url = None
        easy_apply = False
        if self.check_for_easy_apply(job):
            # print('found, skipping.')
            url = job.find_element(
                By.XPATH, EASY_APPLY_URL).get_attribute('href')
            easy_apply = True
        else:
            # print('not found, saving job.')
            job.click()
            time.sleep(.5)

            try:
                apply_button = WebDriverWait(self.driver, timeout=5).until(
                    ec.element_to_be_clickable((By.XPATH, APPLY_NOW_BUTTON)))
                if apply_button:
                    apply_button.click()
                else:
                    print(apply_button)
                    return
            except TimeoutException:
                print(APPLY_BUTTON_TIMEOUT)
                return

        job_url = self._extract_url_from_new_tab(url, easy_apply)
        parsed_job_url = self._parse_indeed_job_url(job_url)

        return parsed_job_url

    def _parse_indeed_job_url(self, job_url):
        parsed_url = urlparse(job_url)

        if f'{parsed_url.scheme}://{parsed_url.hostname}' != self.source.url:
            return job_url

        query_params = {}
        for param in parsed_url.query.split('&'):
            k, v = param.split('=')
            query_params.update({k: v})

        return f'{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}?{"jk=" + query_params["jk"] if query_params.get("jk") else ""}'

    def perform_search(self) -> None:
        try:
            title_field = self.driver.find_element(By.ID, 'text-input-what')
            location_field = self.driver.find_element(By.ID, 'text-input-where')
        except NoSuchElementException:
            print('Error locating search elements')
            exit(0)
        else:
            title_field.clear()
            title_field.send_keys(self.search.title)

            location_field.clear()
            location_field.send_keys(self.search.location)

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
            By.XPATH, LAST_24_HOURS_XPATH).get_attribute('href')
        self.driver.get(date_filter_url)
        time.sleep(1)

    def _select_remote_filter(self):
        remote_filter_url = self.driver.find_element(
            By.XPATH, REMOTE_XPATH).get_attribute('href')
        self.driver.get(remote_filter_url)
        time.sleep(1)

    def _extract_url_from_new_tab(self, url=None, easy_apply=False) -> Optional[str]:
        original_window = self.driver.current_window_handle
        job_url = None

        if url is not None:
            self.driver.switch_to.new_window('tab')
            self.driver.get(url)
        else:
            try:
                self.driver.switch_to.window(self.driver.window_handles[1])
            except IndexError:
                print(f'error: {url}')
                return

        try:
            WebDriverWait(self.driver, timeout=5).until(lambda x: self._check_valid_job_url(self.driver.current_url, easy_apply))
        except TimeoutException:
            print(PAGE_LOAD_TIMEOUT)
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
        num_pages=2,
        title='Software Engineer',
        location='United States',
        email='jameshtowler@gmail.com')
    scraper.scrape()


if __name__ == '__main__':
    main()
