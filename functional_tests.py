from selenium import webdriver
import unittest



class NewVisitorTest(unittest.TestCase):


    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the Test!')

        #Ingresar un item nuevo

        #Escribe "comprar tacho de basura" en un text box

        #cuando apreta 'Enter' se agraga el item con la leyenda
        # 1: Comprar tacho de basura

        #hay otro text-box que la invita a agregar otro item.
        #ingresa: "Tirar la basura".

        #hay otro text-box para usar ingresar otro item.
        #ingresa: "Sacar la basura".

        #la pagina se actualiza, y ahora muestra todos los items de la lista.

        #Se genera un URL con la lista guardada y se explica con un texto.

        #Al visitar ese URL su lista sigue estando ahi.

        #usuario satisfecho.

if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    unittest.main()