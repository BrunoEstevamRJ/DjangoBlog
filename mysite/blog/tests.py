from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class SignUpViewTests(TestCase):
    def test_signup_requires_email(self):
        response = self.client.post(reverse('blog:signup'), {
            'username': 'newuser',
            'email': '',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'This field is required.')
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_signup_saves_email(self):
        response = self.client.post(reverse('blog:signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })

        self.assertRedirects(response, reverse('blog:login'))
        self.assertEqual(
            User.objects.get(username='newuser').email,
            'newuser@example.com',
        )
