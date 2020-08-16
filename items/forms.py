from django import forms
from .models import Borrow

class BorrowForm(Form):
    class Meta:
        model = Borrow
        fields = ()

