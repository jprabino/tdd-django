from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import time
import os
import poplib
import re
import time

from .base import FunctionalTest

# TEST_EMAIL = 'edith@example.com'
SUBJECT = "Tu link de logueo a Superlists"
os.environ['GMAIL_PASSWORD'] = 'n1ur0d0m0t1cs!'
class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):

        if self.staging_server:
            test_email = 'niuro.domotics@yahoo.com'
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.live_server_url)
        # self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertIn('Check your email',
                                            self.browser.find_element_by_tag_name('body').text))

        # email = mail.outbox[0]
        #
        # self.assertIn(TEST_EMAIL, email.to)
        # self.assertEqual(email.subject, SUBJECT)
        body = self.wait_for_email(test_email, SUBJECT)
        self.assertIn('Usa el siguiente link para loguearte', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'No se pudo encontrar la url en el cuerpo del mail:\n{body}')

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        self.browser.get(url)

        # self.wait_to_be_logged_in(email=TEST_EMAIL)
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text('Log Out').click()

        # She is logged out
        # self.wait_to_be_logged_out(email=TEST_EMAIL)
        self.wait_to_be_logged_out(email=test_email)

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['GMAIL_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    # print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
