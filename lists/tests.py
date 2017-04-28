from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from lists.models import Item, List
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



class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'El primero de todos los items de la lista'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Segundo Item'
        second_item.list = list_
        second_item.save()

        seved_list = List.objects.first()
        self.assertEqual(seved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(second_item.list, list_)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'Item nuevo en la lista'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Item nuevo en la lista' )

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'Item nuevo en la lista'})
        self.assertRedirects(response, '/lists/la-unica-lista-del-mundo/')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/la-unica-lista-del-mundo/')

        self.assertTemplateUsed(response,'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemcillo 1', list=list_)
        Item.objects.create(text='itemcillo 2', list=list_)

        response = self.client.get('/lists/la-unica-lista-del-mundo/')

        self.assertContains(response, 'itemcillo 1')
        self.assertContains(response, 'itemcillo 2')
