# from django.test import TestCase
# from django.urls import reverse
# import requests
# from users.models import User
# from .models import Item

# class TestItemLoggedIn(TestCase):
    
#     username = 'a_new_username'
#     password = 'secure_password'

#     def setUp(self):
#         User.objects.create_user(
#             username = self.username,
#             password = self.password
#         )
#         self.client.post(reverse('login'), {'username': self.username, 'password': self.password})



# class TestItemNotLoggedIn(TestCase):
#     username = 'a_new_username'
#     password = 'secure_password'

#     def setUp(self):
#         user = User.objects.create_user(
#             username = self.username,
#             password = self.password
#         )
#         self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
#         Item.objects.create(name = 'umbrella', desc = 'item_desc', quantity = 3, , None)


#     def test_item_search(self):
#         response = self.client.get()

# Create your tests here.
