from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase

from .models import Livro


class LivroValidatorTests(SimpleTestCase):
    def test_titulo_rejeita_menos_de_tres_caracteres(self):
        livro = Livro(titulo='AB', autor='Autor', ano_publicacao=2020)
        with self.assertRaises(ValidationError):
            livro.full_clean()

    def test_ano_rejeita_valores_fora_do_intervalo(self):
        for ano in (1449, 2200):
            with self.subTest(ano=ano):
                livro = Livro(titulo='Livro válido', autor='Autor', ano_publicacao=ano)
                with self.assertRaises(ValidationError):
                    livro.full_clean()

    def test_paginas_rejeita_fora_do_intervalo(self):
        for paginas in (0, 5001):
            with self.subTest(paginas=paginas):
                livro = Livro(titulo='Livro válido', autor='Autor', ano_publicacao=2020, paginas=paginas)
                with self.assertRaises(ValidationError):
                    livro.full_clean()

    def test_isbn_deve_conter_13_digitos(self):
        livro = Livro(titulo='Livro válido', autor='Autor', ano_publicacao=2020, isbn='123ABC')
        with self.assertRaises(ValidationError):
            livro.full_clean()

        livro.isbn = '1234567890123'
        livro.full_clean()


# Create your tests here.
