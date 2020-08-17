from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseForbidden

from .forms import BorrowForm
from .models import Item, Borrow

def my_item_list(request):
    if request.user.is_authenticated:
        my_items = Item.objects.filter(
            owner = request.user
            )
        
        my_items_id = my_items.values_list(
                'pk', flat=True
            )

        all_item_borrowed = Borrow.objects.filter(
            item_borrowed__in = my_items_id
        )

        borrowed_item_records = all_item_borrowed.select_related(
                'item_borrowed'
            )

        available_items = my_items.filter(
            item_borrow_record__isnull=True
        )

        return render(request, 'item_list.html', {'items_list': available_items, 'borrowed_item_records' : borrowed_item_records})
    else:
        return redirect(reverse_lazy('login'))

class ItemDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'item'
    model = Item
    template_name = 'item_detail.html'

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
        num_of_item_borrow_rec = Borrow.objects.filter(
            item_borrowed=self.get_object()
        ).count()

        return self.request.user == self.get_object().owner and num_of_item_borrow_rec == 0

def item_search_view(request):
    search_query = request.GET.get('search_query')
    
    result = Item.objects.filter(
        Q(name__contains=search_query)
        ).exclude(
            item_borrow_record__isnull=False
        )

    if request.user.is_authenticated:
        result = result.exclude(
                owner=request.user
            )

    return render(request, 'item_search.html', {'items_list' : result, 'items_count' : result.count(), 'query' : search_query})

def item_borrow_view(request, pk):
    
    if (not request.user.is_authenticated):
        return redirect(reverse_lazy('login'))

    item = Item.objects.get(pk = pk)
    if (request.user == item.owner):
        return HttpResponseForbidden()

    form = BorrowForm
    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            print(form.cleaned_data['return_date'], 'hello')
            new_borrow = Borrow(
                quantity=form.cleaned_data['quantity'], 
                return_date=form.cleaned_data['return_date'],
                borrower=request.user,
                item_borrowed=item,
            )
            new_borrow.save()
        return redirect(reverse_lazy('items_list'))
    template_name = 'item_borrow.html'


    return render(request, template_name, {'form': form, 'item' : item})



class ItemReturnView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Borrow
    context_object_name = 'item'
    fields = []
    template_name = 'item_return.html'
    success_url = reverse_lazy('items_list')
    def test_func(self):
        return self.request.user == self.get_object().item_borrowed.owner

def item_borrowed_view(request):
    result = Borrow.objects.filter(
        borrower=request.user
    ).select_related(
        'item_borrowed'
    )

    return render(request, 'item_borrowed.html', {'borrow_records' : result})

# Create your views here.
