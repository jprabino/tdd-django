from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from lists.views import home_page
from django.test import TestCase
from django.http import HttpRequest

# Create your tests here.

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data = {'item_text': 'Item nuevo en la lista'})
        self.assertIn('Item nuevo en la lista', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
