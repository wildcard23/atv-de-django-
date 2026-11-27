from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='leitor@example.com',
            username='leitor',
            password='Senha-forte-123',
        )

    def test_login_uses_email_and_redirects_to_book_list(self):
        response = self.client.post(
            reverse('users:login'),
            {'username': self.user.email.upper(), 'password': 'Senha-forte-123'},
        )

        self.assertRedirects(response, reverse('livros:lista'), fetch_redirect_response=False)

    def test_logout_redirects_to_login(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('users:logout'))

        self.assertRedirects(response, reverse('users:login'), fetch_redirect_response=False)

    def test_signup_requires_unique_email_and_saves_lowercase(self):
        response = self.client.post(
            reverse('users:signup'),
            {
                'username': 'nova-leitora',
                'email': 'NOVA@EXAMPLE.COM',
                'password1': 'Uma-senha-segura-123',
                'password2': 'Uma-senha-segura-123',
            },
        )

        self.assertRedirects(response, reverse('users:login'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(email='nova@example.com').exists())

        duplicate = self.client.post(
            reverse('users:signup'),
            {
                'username': 'outra-leitora',
                'email': 'LEITOR@EXAMPLE.COM',
                'password1': 'Uma-senha-segura-123',
                'password2': 'Uma-senha-segura-123',
            },
        )
        self.assertEqual(duplicate.status_code, 200)
        self.assertIn('email', duplicate.context['form'].errors)

    def test_authenticated_user_is_redirected_away_from_login(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('users:login'))

        self.assertRedirects(response, reverse('livros:lista'), fetch_redirect_response=False)

    def test_header_shows_authentication_actions_for_visitors_and_user_for_members(self):
        response = self.client.get(reverse('users:login'))
        self.assertContains(response, 'Cadastre-se')
        self.assertContains(response, 'Entrar')

        self.client.force_login(self.user)
        response = self.client.get(reverse('livros:lista'))
        self.assertContains(response, self.user.username)
        self.assertContains(response, 'Sair')

    def test_admin_add_form_uses_custom_user_fields(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='Senha-forte-123',
        )
        self.client.force_login(admin_user)

        response = self.client.get('/admin/users/user/add/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="email"')

        response = self.client.get(f'/admin/users/user/{admin_user.pk}/change/')
        self.assertEqual(response.status_code, 200)
