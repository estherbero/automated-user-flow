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

    @classmethod
    def tearDownClass(self):
      self.page.close()

    def test_login(self):   
        # Go to login page
        self.page.click_elem('//*[@id="nav"]/ul/li[6]/a')

        # Enter credentials and log in
        self.page.set_email(self.email)
        self.page.set_password(self.password)
        self.page.log_in()
        # Wait until Home page is loaded, if it does not load in 10 secs test will fail
        self.page.wait_for_page_title("Home - Hudl", 10)
    
    def test_upload_video(self):
        # Go to Upload page
        # I should use @data-qa-id here and for all other selectors, but for some reason I need to figure out 
        # why when getting the element, this is not interactable. TODO
        # Using Xpath as a workaround, even when this is not reliable and likely to break 
        # Also define vars with selector to improve readability
        # upload_page_sel = 'webnav-globalnav-upload' # this would be the selector using @data-qa-id
        upload_page_sel = '//*[@id="ssr-webnav"]/div/div[1]/nav[1]/div[4]/a[1]/span' # this is the xpath selector
        self.page.click_elem(upload_page_sel) 

        # Click upload file
        upload_button_sel = '//*[@id="web-uploader-app"]/div/section/div/div/div/div/div[2]/div[2]/div[1]/button/span'
        self.page.click_elem(upload_button_sel)
        # Select local video file
        file_to_upload = os.getcwd() + '/res/videoR01.mov'
        upload_file_path_sel = '//*[@id="web-uploader-app"]/div/section/div/div/div/div/div[2]/div[2]/div[1]/input'
        self.page.input_text(upload_file_path_sel, file_to_upload)

        # Wait for upload to complete (automatically shared with all team members by default, we could also include an 
        # specific test for sharing with specific groups, is it OK this way??). It has 90 seconds to complete the 
        # upload for a 15.7 MB file, otherwise it will fail
        self.page.wait_for_file_to_upload(90)
        # Save uploaded file, the file name will be a 6 chars random string to make sure it is unique
        file_name = self.page.save_file()

        # Go to Library page
        library_page_sel = '//*[@id="ssr-webnav"]/div/div[1]/nav[2]/div[3]/a[1]'
        self.page.click_elem(library_page_sel)
        self.page.wait_for_page_title("Library - Hudl", 10)

        # It gets some time to load the video library, if the video is not properly loaded in 20 secs, it will fail
        # We get all the video elements, but we need to make sure we retrieve more than one element since the first
        # one loaded is 'Filter by' element
        elems = self.page.get_elems('uni-subhead')
        cont = 0
        while len(elems) <= 1 and cont < 5:
          time.sleep(4)
          cont += 1
          elems = self.page.get_elems('uni-subhead')
        # Once videos haven been properly loaded, it is time to check if the video just uploaded is present
        video_uploaded = False
        for e in elems:
          if e.text == file_name:
            video_uploaded = True
            break
        self.assertTrue(video_uploaded)

if __name__ == "__main__":
    unittest.main()
