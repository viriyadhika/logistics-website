from django import forms
from .models import Borrow, Item
from django.core.validators import MinValueValidator 
from django.core.exceptions import ValidationError
from tempus_dominus.widgets import DatePicker
from datetime import date

def no_past_date(value):
    today = date.today()
    if value < today:
        raise ValidationError('Return date cannot be in the past')

class BorrowForm(forms.Form):
    return_date = forms.DateField(
        required=True,
        widget=DatePicker(),
        validators=[no_past_date]
    )

    quantity = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(1)],
    )

class ItemNewForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'desc', 'quantity')
        labels = {
            'name' : 'Item Name',
            'desc' : 'Description',
            'quantity' : 'Quantity',
        }


