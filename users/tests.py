from django.test import TestCase
from .models import User

class TestUserApp:(TestCase)
    username = 'random_user'
    password = 'great password'
    email = 'an_email@mail.com'
    
    def setUp:
        User.objects.create(
            username = self.username, 
            password = self.password,
            email = self.email
            )
        




# Create your tests here.
