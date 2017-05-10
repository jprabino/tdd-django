from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
import os
from unittest import skip



class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        #se ingresa un valor vacio
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        #se refresca la pagina y muestra un error diciendo que debe ingresar un valor
        self.wait_for(lambda : self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                         'No se puede ingresar un item vacío'
                         ))
        #ahora reintenta con un item, y funciona
        self.browser.find_element_by_id('id_new_item').send_keys('Comprar leche')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar leche')

        #ahora reintenta con un espacio en blanco
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        #se recibe una alerta nueva
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        #finalmente ingresa correctamente
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

        self.fail('Test Finalizado')