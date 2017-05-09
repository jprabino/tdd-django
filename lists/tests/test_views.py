import time
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

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'Item nuevo en la lista'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Item nuevo en la lista' )

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'Item nuevo en la lista'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'Nuevo item de una lista existente'}
                         )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nuevo item de una lista existente')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'Nuevo item de una lista existente',})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()

        response = self.client.get(f'/lists/{list_.id}/')

        self.assertTemplateUsed(response,'list.html')


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemcillo 1', list=correct_list)
        Item.objects.create(text='itemcillo 2', list=correct_list)
        another_correct_list = List.objects.create()
        Item.objects.create(text='otro itemcillo 1', list=another_correct_list)
        Item.objects.create(text='otro itemcillo 2', list=another_correct_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemcillo 1')
        self.assertContains(response, 'itemcillo 2')
        self.assertNotContains(response, 'otro itemcillo 1')
        self.assertNotContains(response, 'otro itemcillo 2')

    def test_passes_correct_list_to_template(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)