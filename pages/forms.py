from django.forms import Form, CharField

class SearchBarForm(Form):
    item_to_search = CharField(max_length=140)

