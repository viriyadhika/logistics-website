from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Item(models.Model):
    name = models.CharField(max_length=140)
    desc = models.TextField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='item_owned'
    )


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_detail', args=[str(self.id)])

class Borrow(models.Model):
    borrower = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    item_borrowed = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_query_name='item_borrow_record'
    )

    borrow_date = models.DateField(
        auto_now_add=True,
    )

    return_date = models.DateField(
        blank=True,
        null=True,
    )

    quantity = models.IntegerField(
        blank=True,
        null=True,
    )
    

    def __str__(self):
        return (str(self.item_borrowed) + ' by ' + str(self.borrower.username))

    def get_absolute_url(self):
        return reverse('borrow_detail', args=[str(self.id)])



# Create your models here.
