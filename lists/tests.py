from django.test import TestCase

# Create your tests here.

class TestDepruebaDelTestEngine(TestCase):

    def test_nose_sumar(self):

        self.assertEqual(1+1, 3)