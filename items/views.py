from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseForbidden


from .models import Item

def my_item_list(request):
    if request.user.is_authenticated:
        all_items = Item.objects.filter(
            owner = request.user
            ).order_by(
                'borrower'
            )
        return render(request, 'item_list.html', {'items_list': all_items})
    else:
        return redirect(reverse_lazy('login'))

class ItemDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'item'
    model = Item
    template_name = 'item_detail.html'

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items_list'

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'item_new.html'
    fields = ['name', 'desc', 'quantity']
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    context_object_name = 'item'
    template_name = 'item_delete.html'
    success_url = reverse_lazy('items_list')
    def test_func(self):
        return self.request.user == self.get_object().owner

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    context_object_name = 'item'
    model = Item
    template_name = 'item_update.html'
    fields = ['name', 'desc', 'quantity']

    def test_func(self):
        return self.request.user == self.get_object().owner and self.get_object().borrower == None

def item_search_view(request):
    search_query = request.GET.get('search_query')
    result = Item.objects.filter(
        Q(name__contains=search_query)
            ).filter(
                borrower=None
            )

    if request.user.is_authenticated:
        result = result.exclude(
                owner=request.user
            )

    return render(request, 'item_search.html', {'items_list' : result, 'items_count' : result.count(), 'query' : search_query})

class ItemBorrowView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item 
    context_object_name = 'item'
    fields = []
    template_name = 'item_borrow.html'
    def test_func(self):
        return self.request.user != self.get_object().owner
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
