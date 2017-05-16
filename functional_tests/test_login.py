from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import time

from .base import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = "Tu link de logueo a Superlists"

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertIn('Check your email',
                                            self.browser.find_element_by_tag_name('body').text))

        email = mail.outbox[0]

        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        self.assertIn('Usa el siguiente link para loguearte', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'No se pudo encontrar la url en el cuerpo del mail:\n{email.body}')

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        self.browser.get(url)
        self.wait_for(lambda : self.browser.find_element_by_link_text('Log Out')
                      )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)