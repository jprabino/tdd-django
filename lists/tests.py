from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from lists.models import Item
from lists.views import home_page
from django.test import TestCase
from django.http import HttpRequest

# Create your tests here.

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'Item nuevo en la lista'})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Item nuevo en la lista' )

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'Item nuevo en la lista'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/la-unica-lista-del-mundo/')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'El primero de todos los items de la lista'
        first_item.save()

        second_item = Item()
        second_item.text = 'Segundo Item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(second_saved_item.text, second_item.text)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/la-unica-lista-del-mundo/')

        self.assertTemplateUsed(response,'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemcillo 1')
        Item.objects.create(text='itemcillo 2')

        response = self.client.get('/lists/la-unica-lista-del-mundo/')

        self.assertContains(response, 'itemcillo 1')
        self.assertContains(response, 'itemcillo 2')
