import time
import os
import random
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class Page:
    def __init__(self):
      self.driver = webdriver.Chrome()

    def go(self, url):
      self.driver.get(url)

    def close(self):
      self.driver.close()
    
    def wait_for_page_title(self, title, timeout):
      WebDriverWait(self.driver, timeout).until(EC.title_is(title))
    
    def wait_for_elem(self, selector, timeout):
      WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, selector)))
        
    def get_elem(self, selector):
      # Ideally we should use @data-qa-id custom attribute in order to make our test suite steady and robust
      # and also tests way more clear and easy to mantain
      # For this task, we mostly filter by xpath. Even though we still define @data-qa-id selector.
      if selector[:2] == '//': # This filters xpath selector
        return self.driver.find_element_by_xpath(selector)
      else:
        # This is the best option since we have control from QA side
        return self.driver.find_element_by_css_selector("a[data-qa-id='" + selector + "']")

    def set_email(self, email):
      self.driver.find_element_by_id('email').send_keys(email)
    
    def set_password(self, pwd):
      self.driver.find_element_by_id('password').send_keys(pwd)

    def log_in(self):
      self.driver.find_element_by_id('logIn').click()
    
    def get_elems(self, selector):
      return self.driver.find_elements_by_class_name(selector)

    def click_elem(self, selector):
      self.get_elem(selector).click()

    def input_text(self, selector, text):
      self.get_elem(selector).send_keys(text)

    def create_random_string(self, length):
      return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(length)])
    
    def wait_for_file_to_upload(self, timeout):
        # Using xpath to get element which summarizes whether upload is in process or complete
        self.wait_for_elem('//*[@id="web-uploader-app"]/div/section/div/div/div[1]/div/div[1]/h3', 10)
        elem = self.get_elem('//*[@id="web-uploader-app"]/div/section/div/div/div[1]/div/div[1]/h3')
        # For some reason I get a more stable result using my own "wait until" than WebDriverWait, to investigate
        cont = 0
        while elem.text != "Upload Complete" and cont < timeout:
            elem = self.get_elem('//*[@id="web-uploader-app"]/div/section/div/div/div[1]/div/div[1]/h3')
            time.sleep(1)
            cont += 1

    def save_file(self):
      # Create a 6 characters random string
      file_name = self.create_random_string(6)
      self.input_text('//*[@id="video-name__text-input"]', file_name)
      self.click_elem('//*[@id="web-uploader-app"]/div/section/div/div/section/div[1]/div[2]/div[6]/div/button')
      return file_name
