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
      # Ideally we should have test IDs in the HTML in order to make our test suite steady and robust
      # and also tests way more clear and easy to mantain
      # These test IDs should be only used for testing porpouses so we avoid some dev can remove them
      # For this task, we just filter by xpath and id
      if selector[:1] == '/': #[:1] --> substring, first part of the path
        #WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, selector)))
        return self.driver.find_element_by_xpath(selector)
      elif selector == 'email' or selector == 'password' or selector == 'logIn':
        return self.driver.find_element_by_id(selector)
      else:
        return self.driver.find_element_by_css_selector("a[data-qa-id='" + selector + "']")
    
    def get_elems(self, selector):
      return self.driver.find_elements_by_class_name(selector)

    def click_elem(self, selector):
      self.get_elem(selector).click()

    def input_text(self, selector, text):
      self.get_elem(selector).send_keys(text)

    def create_random_string(self):
      return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
    
    def wait_for_file_to_upload(self, timeout):
        self.wait_for_elem('//*[@id="web-uploader-app"]/div/section/div/div/div[1]/div/div[1]/h3', 10)
        elem = self.get_elem('//*[@id="web-uploader-app"]/div/section/div/div/div[1]/div/div[1]/h3')
        cont = 0
        while elem.text != "Upload Complete" and cont < timeout:
            elem = self.get_elem('//*[@id="web-uploader-app"]/div/section/div/div/div[1]/div/div[1]/h3')
            time.sleep(1)
            cont = cont + 1

    def save_file(self):
      file_name = self.create_random_string()
      self.input_text('//*[@id="video-name__text-input"]', file_name)
      self.click_elem('//*[@id="web-uploader-app"]/div/section/div/div/section/div[1]/div[2]/div[6]/div/button')
      return file_name