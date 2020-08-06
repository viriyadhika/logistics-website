from django.test import TestCase
from .models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

class TestUserApp(TestCase):
    username = 'random_user'
    username1 = 'another_random_user'
    password = 'great password'
    email = 'an_email@mail.com'
    email1 = 'another_email@mail.com'

    def test_signup_status_code(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('signup.html')

    def test_signup_form(self):
        response = self.client.post(
            reverse('signup'),
            {'username' : self.username,
            'password1' : self.password,
            'password2' : self.password,
            'email' : self.email
            })
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)

        #Same username
        response1 = self.client.post(
            reverse('signup'),
            {'username' : self.username,
            'password1' : self.password,
            'password2' : self.password,
            'email' : self.email1
            })
        self.assertEqual(get_user_model().objects.all().count(), 1)
        
        #Same email
        response2 = self.client.post(
            reverse('signup'),
            {'username' : self.username1,
            'password1' : self.password,
            'password2' : self.password,
            'email' : self.email
            })
        self.assertEqual(get_user_model().objects.all().count(), 1)

        #Different user
        response3 = self.client.post(
            reverse('signup'),
            {'username' : self.username1,
            'password1' : self.password,
            'password2' : self.password,
            'email' : self.email1
            })
        self.assertEqual(get_user_model().objects.all().count(), 2)

# Create your tests here.
