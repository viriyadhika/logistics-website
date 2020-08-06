from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 

from .models import Item

def my_item_list(request):
    if request.user.is_authenticated:
        all_items = Item.objects.filter(owner = request.user)
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

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    context_object_name = 'item'
    template_name = 'item_delete.html'
    success_url = reverse_lazy('items_list')

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    context_object_name = 'item'
    model = Item
    template_name = 'item_update.html'
    fields = ['name', 'desc', 'quantity']

def item_search_view(request):
    searched_item =Item.objects.filter(name__contains=)

# Create your views here.
