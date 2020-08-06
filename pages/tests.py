from django.test import SimpleTestCase
from django.urls import reverse


class TestHomePage(SimpleTestCase):
    
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

# Create your tests here.
