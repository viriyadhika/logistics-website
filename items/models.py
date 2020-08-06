from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Item(models.Model):
    name = models.CharField(max_length=140)
    desc = models.TextField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_detail', args=[str(self.id)])


# Create your models here.
