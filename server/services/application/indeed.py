import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from server.models import Job
from server.repositories import JobRepository
from server.services.base import BaseService
from server.services.scrapers.helper_funcs.selenium import handle_sign_in


class IndeedApplicationService(BaseService):
    def __init__(self, *args, **kwargs):
        self.options.update(kwargs)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

    def apply(self, job: Job):
        self.source = job.source if job.source.name == 'indeed' else None
        if self.source is None:
            raise AttributeError('Source does not match service source. Source must be Indeed.')

        self.driver.get(job.source.url)
        time.sleep(1)

        handle_sign_in(self)
        self._apply(job)

    def _apply(self, job):
        self.driver.switch_to.new_window('tab')
        self.driver.get(job.url)

        WebDriverWait(self.driver, timeout=5).until(ec.element_to_be_clickable(
            (By.XPATH, '//button[@id="indeedApplyButton"]')))
        self.driver.find_element(By.XPATH, '//button[@id="indeedApplyButton"]').click()

    def _review_location(self):
        try:
            self.driver.find_element(By.XPATH, '//h1[text()="Review your location details from your profile"]')
        except NoSuchElementException:
            return
        else:
            self.driver.find_element(By.XPATH, '//*[@id="input-city"]').send_keys("Richmond, VA")
            self.driver.find_element(By.XPATH, '//*[@id="input-postalCode"]').send_keys('23060')
            self.driver.find_element(By.XPATH, '//button[.//span[text()="Continue"]]').click()

    def _choose_resume(self):
        try:
            self.driver.find_element(By.XPATH, '//h1[text()="Add a resume for the employer"]')
        except NoSuchElementException:
            return
        else:
            self.driver.find_element(By.XPATH, '//div[@data-testid="FileResumeCard"]').click()
            self.driver.find_element(By.XPATH, '//button[.//span[text()="Continue"]]').click()


job_repo = JobRepository()
job = job_repo.get_by_id(7)

# print(job.source)

indeed_app_service = IndeedApplicationService(email='jameshtowler@gmail.com')
indeed_app_service.apply(job)