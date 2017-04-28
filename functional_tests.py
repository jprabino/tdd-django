from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ingresar un item nuevo
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Ingresar un nuevo item a la lista'
                         )
        # Escribe "comprar tacho de basura" en un text box
        inputbox.send_keys('comprar tacho de basura')
        # cuando apreta 'Enter' se agraga el item con la leyenda
        # 1: Comprar tacho de basura
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: comprar tacho de basura', [row.text for row in rows])
        # hay otro text-box que la invita a agregar otro item.
        # ingresa: "Tirar la basura".

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Tirar la basura')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: comprar tacho de basura', [row.text for row in rows])
        self.assertIn('2: Tirar la basura', [row.text for row in rows])
        self.fail('Tests terminados!')

        # hay otro text-box para usar ingresar otro item.
        # ingresa: "Sacar la basura".

        # la pagina se actualiza, y ahora muestra todos los items de la lista.

        # Se genera un URL con la lista guardada y se explica con un texto.

        # Al visitar ese URL su lista sigue estando ahi.

        # usuario satisfecho.

if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    unittest.main()
