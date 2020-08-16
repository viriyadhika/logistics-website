from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Borrow
from items.models import Item
from django.contrib.contenttypes.models import ContentType

def item_borrow_view(request, pk):
    Item.objects.get(pk = pk)
    

class ItemBorrowView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Borrow
    context_object_name = 'item'
    fields = []
    template_name = 'item_borrow.html'
    def test_func(self):
        return self.request.user != Item.objects.get()
    def form_valid(self, form):
        form.instance.borrower = self.request.user
        return super().form_valid(form)

class ItemReturnView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    context_object_name = 'item'
    fields = []
    template_name = 'item_return.html'
    def test_func(self):
        return self.request.user == self.get_object().owner and self.get_object().borrower != None
    def form_valid(self, form):
        form.instance.borrower = None
        return super().form_valid(form)

def item_borrowed_view(request):
    result = Item.objects.filter(
        borrower=request.user
    )
    return render(request, 'item_borrowed.html', {'items_list' : result})


# Create your views here.
