from django import forms
from .models import Borrow
from tempus_dominus.widgets import DatePicker

class BorrowForm(forms.Form):
    return_date = forms.DateField(
        required=True,
        widget=DatePicker(),
    )

    quantity = forms.IntegerField(
        required=True
    )
