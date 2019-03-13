import time
import unittest
import os
from pages.page import Page

class PythonOrgSearch(unittest.TestCase):
    # Credentials for login
    # If running in local, please define your credentials in env vars, or replace these lines with the proper ones
    email = os.environ.get('EMAIL') 
    password = os.environ.get('PASSWORD')

    @classmethod
    def setUpClass(self):
      self.page = Page()
      self.page.go('https://hudl.com/')
        # self.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(self):
      self.page.close()

    def test_login(self):   
        # Go to login page
        self.page.click_elem('//*[@id="nav"]/ul/li[6]/a')

        # Enter credentials and log in
        self.page.input_text('email', self.email)
        self.page.input_text('password', self.password)
        self.page.click_elem('logIn')
        # Wait until Home page is loaded, if it does not load in 10 secs tes will fail
        self.page.wait_for_page_title("Home - Hudl", 10)
    
    def test_upload_video(self):
        # Go to Upload page
        self.page.click_elem('//*[@id="ssr-webnav"]/div/div[1]/nav[1]/div[4]/a[1]/span')
        # elem = self.get_elem('webnav-globalnav-upload')
        # element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa-id='webnav-globalnav-upload']")))
        # self.get_elem('webnav-globalnav-upload').click()

        # Click upload file
        self.page.click_elem('//*[@id="web-uploader-app"]/div/section/div/div/div/div/div[2]/div[2]/div[1]/button/span')
        # Select local video file
        # actions = ActionChains(browser)
        file_to_upload = os.getcwd() + '/res/videoR01.mov'
        self.page.input_text('//*[@id="web-uploader-app"]/div/section/div/div/div/div/div[2]/div[2]/div[1]/input', file_to_upload)

        #wait upload completed (automatically shared with all team members by default)
        # element = WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="web-uploader-app"]/div/section/div/div/div[1]/div/div[1]/h3')))
        self.page.wait_for_file_to_upload(90)
        # element = WebDriverWait(browser, 60).until(elem.text == "Upload Complete")

        # elem = browser.find_element_by_xpath('//*[@id="ssr-webnav"]/div/div[1]/nav[1]/div[2]/a[1]/span')
        # elem.click()

        file_name = self.page.save_file()

        
        # self.click_elem('//*[@id="permissions-details"]/div[1]/button')
        # Go to Video page
        self.page.click_elem('//*[@id="ssr-webnav"]/div/div[1]/nav[2]/div[3]/a[1]')

        # It gets some time to load video library, if video it is not properly loaded in 10 secs, it will fail
        self.page.wait_for_page_title("Library - Hudl", 10)
        elems = self.page.get_elems('uni-subhead')
        cont = 0
        while len(elems) <= 1 and cont < 5:
          time.sleep(3)
          cont = cont + 1
          elems = self.page.get_elems('uni-subhead')
        # Once videos haven been properly loaded, it is time to check the video just uploaded in the test
        video_uploaded = False
        for e in elems:
          if e.text == file_name:
            video_uploaded = True
            break
        self.assertTrue(video_uploaded)
        # elem = self.get_elem('//*[@id="modalTitle"]')
        # actions.move_to_element(elem)
        # actions.click(elem)
        # actions.perform()
        # # self.driver.find_element_by_xpath('//input[@data-qa-id="permissions-entry-field_multi-select-input"]')

        # time.sleep(3)
        # actions.send_keys(Keys.DOWN * 4)  
        # actions.perform()
        # actions.send_keys(Keys.ENTER)  
        # actions.perform()
        # actions.send_keys(Keys.TAB * 5)  
        # actions.perform()
        # actions.send_keys(Keys.ENTER)  
        # actions.perform()
        # time.sleep(3)
        # self.click_elem('//*[@id="App"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/li[1]/span/div/div/div[2]/div[1]/span')
        #self.input_text('permissions-entry-field__multi-select-input', self.team)

        # self.input_text('video-name__text-input', 'match_video_test')
        # self.click_elem('video-details__save-and-continue-btn')
        # self.click_elem('permissions-modal__modal-content')
        # self.input_text('permissions-entry-field__multi-select-input', self.team)

        #share video with team
        #to review
        # self.click_elem('//*[@id="permissions-details"]/div[1]/button')
        # self.input_text('//*[@id="uniId_3847-input"]', self.team)
        # self.click_elem('/html/body/div[8]/div/div/div[3]/div/button')

        # self.click_elem('//*[@id="web-uploader-app"]/div/section/div/div/div[1]/div/div[1]/h3')
        # self.input_text('//*[@id="uniId_70-input"]', self.team)
        # self.click_elem('//html/body/div[9]/div/div/div[3]/div/button')


if __name__ == "__main__":
    unittest.main()
