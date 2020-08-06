from django.db import models
from items.models import Item
from django.contrib.auth import get_user_model
from django.urls import reverse

class Borrow(models.Model):
    borrower = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    item_borrowed = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return (str(self.item_borrowed) + ' by ' + str(self.borrower.username))

    def get_absolute_url(self):
        return reverse('borrow_detail', args=[str(self.id)])


# Create your models here.
