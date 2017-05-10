from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
import os
from unittest import skip



class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        #se ingresa un valor vacio
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        #se refresca la pagina y muestra un error diciendo que debe ingresar un valor
        # self.wait_for(lambda : self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
        #                  'No se puede ingresar un item vacío'
        #                  ))

        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))
        # self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
        #                                        'No se puede ingresar un item vacío'
        #                                        ))
        #ahora reintenta con un item, y funciona
        self.get_item_input_box().send_keys('Comprar leche')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar leche')

        #ahora reintenta con un espacio en blanco
        self.get_item_input_box().send_keys(Keys.ENTER)

        #el browser no va a tomar la lista ahora
        self.wait_for_row_in_list_table('1: Comprar leche')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        #finalmente ingresa correctamente
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar leche')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):

        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys('sacar fotos')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: sacar fotos')

        self.get_item_input_box().send_keys('sacar fotos')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda : self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                                                "Ya se encuentra el item en la lista"
                                                ))