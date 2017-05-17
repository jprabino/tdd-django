from selenium.webdriver.common.keys import Keys

from lists.forms import DUPLICATE_ITEM_ERROR
from .base import FunctionalTest
import os
from unittest import skip



class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
    def test_cannot_add_empty_list_items(self):

        #se ingresa un valor vacio
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

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

        self.add_list_item('sacar fotos')

        self.get_item_input_box().send_keys('sacar fotos')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda : self.assertEqual(self.get_error_element().text,
                                                DUPLICATE_ITEM_ERROR
                                                ))

    def test_error_messages_are_cleared_on_input(self):

        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        self.get_item_input_box().send_keys('a')

        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))