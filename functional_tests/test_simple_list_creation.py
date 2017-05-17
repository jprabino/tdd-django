from unittest import skip

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ingresar un item nuevo
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Nueva Tarea a realizar'
                         )
        self.add_list_item('comprar tacho de basura')

        # hay otro text-box que la invita a agregar otro item.
        # ingresa: "Tirar la basura".

        self.add_list_item('Tirar la basura')
        self.wait_for_row_in_list_table('1: comprar tacho de basura')
        self.wait_for_row_in_list_table('2: Tirar la basura')
        # hay otro text-box para usar ingresar otro item.
        # ingresa: "Sacar la basura".

        # la pagina se actualiza, y ahora muestra todos los items de la lista.

        # Se genera un URL con la lista guardada y se explica con un texto.

        # Al visitar ese URL su lista sigue estando ahi.

        # usuario satisfecho.

    def test_multiple_users_can_start_lists_at_different_urls(self):

        self.browser.get(self.live_server_url)
        self.add_list_item('comprar tacho de basura')

        current_user_list_url = self.browser.current_url
        self.assertRegex(current_user_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('comprar tacho de basura', page_text)
        self.assertNotIn('Tirar la basura', page_text)


        self.add_list_item('ir al dentista')

        new_user_list_url  = self.browser.current_url
        self.assertRegex(new_user_list_url, '/lists/.+')
        self.assertNotEqual(new_user_list_url,current_user_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('comprar tacho de basura', page_text)
        self.assertIn('ir al dentista', page_text)
