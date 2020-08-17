from django.forms import Form
from .models import Borrow

class BorrowForm(Form):
    class Meta:
        model = Borrow
        fields = ()

