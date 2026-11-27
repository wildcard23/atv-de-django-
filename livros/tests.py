from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
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


class LivroAuthorizationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            email='dona@example.com',
            username='dona',
            password='Senha-forte-123',
        )
        self.other_user = user_model.objects.create_user(
            email='outro@example.com',
            username='outro',
            password='Senha-forte-123',
        )
        self.livro = Livro.objects.create(
            titulo='Livro de teste',
            autor='Autora',
            ano_publicacao=2020,
            registered_by=self.owner,
        )

    def test_library_pages_require_authentication(self):
        urls = [
            '/',
            '/novo/',
            f'/{self.livro.pk}/',
            f'/{self.livro.pk}/editar/',
            f'/{self.livro.pk}/excluir/',
            '/sobre/',
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f'/users/login/?next={url}',
                    fetch_redirect_response=False,
                )

    def test_book_creator_can_update_and_delete_but_other_user_cannot(self):
        self.client.force_login(self.other_user)
        edit_url = f'/{self.livro.pk}/editar/'
        delete_url = f'/{self.livro.pk}/excluir/'

        self.assertEqual(self.client.get(edit_url).status_code, 404)
        self.assertEqual(self.client.post(edit_url).status_code, 404)
        self.assertEqual(self.client.get(delete_url).status_code, 404)
        self.assertEqual(self.client.post(delete_url).status_code, 404)
        self.assertTrue(Livro.objects.filter(pk=self.livro.pk).exists())

        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(edit_url).status_code, 200)
        self.assertEqual(self.client.get(delete_url).status_code, 200)

    def test_create_records_authenticated_user_as_owner(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            '/novo/',
            {
                'titulo': 'Novo título',
                'autor': 'Novo autor',
                'ano_publicacao': 2021,
                'paginas': '',
                'isbn': '',
                'disponivel': 'on',
            },
        )

        self.assertRedirects(response, '/')
        new_book = Livro.objects.get(titulo='Novo título')
        self.assertEqual(new_book.registered_by, self.other_user)
