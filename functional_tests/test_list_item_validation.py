from .base import FunctionalTest
import os
from unittest import skip

MAX_WAIT = 3
STAGING_SERVER="10.210.8.206"
os.environ['STAGING_SERVER']=STAGING_SERVER


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        #se ingresa un valor vacio

        #se refresca la pagina y muestra un error diciendo que debe ingresar un valor

        #ahora reintenta con un item, y funciona

        #ahora reintenta con un espacio en blanco

        #se recibe una alerta nueva

        #finalmente ingresa correctamente

        self.fail('write me!')