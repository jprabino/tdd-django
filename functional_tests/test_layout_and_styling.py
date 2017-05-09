from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
import os

MAX_WAIT = 3
STAGING_SERVER="10.210.8.206"
os.environ['STAGING_SERVER']=STAGING_SERVER

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        #Edith va a la home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,
                               512,
                               delta=10
                               )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
