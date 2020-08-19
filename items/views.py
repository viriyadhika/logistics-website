from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Sum
from django.http import HttpResponseForbidden
from django.db.models.functions import Coalesce

from .forms import BorrowForm
from .models import Item, Borrow

def my_item_list(request):
    class Item_and_Borrower:
        def __init__(self, item, available_quantity):
            self.item = item
            self.available_quantity = available_quantity
            self.borrow = []

        def add_borrow_record(self, borrow_record):
            self.borrow.append(borrow_record)

        def set_available_quantity(self, available_quantity):
            self.available_quantity = available_quantity 

    if request.user.is_authenticated:
        borrowed_item_records = Borrow.objects.filter(
                item_borrowed__owner = request.user
            ).select_related(
                'item_borrowed'
            )

        my_items = list(
                Item.objects.filter(
                    owner=request.user
                )
            )

        my_borrowed_items = list(
                Borrow.objects.filter(
                    item_borrowed__in = my_items
                ).order_by(
                    'return_date'
                )
            )

        result = []

        for my_item in my_items:
            available_quantity = my_item.quantity
            item_and_borrower = Item_and_Borrower(my_item, available_quantity)
            for borrow_item in my_borrowed_items:
                if borrow_item.item_borrowed == my_item:
                    item_and_borrower.set_available_quantity(
                        item_and_borrower.available_quantity - borrow_item.quantity
                    )
                    item_and_borrower.add_borrow_record(borrow_item)

            result.append(item_and_borrower)

        return render(request, 'item_list.html', {
            'items_and_borrower': result,
            'borrowed_item_records' : borrowed_item_records })
    else:
        return redirect(reverse_lazy('login'))




# def my_item_list(request):
#     class Item_and_Available:
#         def __init__(self, item, available_quantity):
#             self.item = item
#             self.available_quantity = available_quantity

#     if request.user.is_authenticated:
#         borrowed_item_records = Borrow.objects.filter(
#                 item_borrowed__owner = request.user
#             ).select_related(
#                 'item_borrowed'
#             )

#         borrowed_item_aggregate = borrowed_item_records.values(
#                 'item_borrowed'
#             ).annotate(
#                 Sum('quantity')
#             )

#         my_items = Item.objects.filter(
#                 owner = request.user
#             )
#         available_items = []


#         for my_item in list(my_items):
#             available_quantity = my_item.quantity
#             for a_borrowed_item in borrowed_item_aggregate.values('item_borrowed_id', 'quantity'):
#                 if a_borrowed_item['item_borrowed_id'] == my_item.id:
#                     available_quantity = my_item.quantity - a_borrowed_item['quantity']
#                     break
#             if (available_quantity > 0):
#                 available_items.append(Item_and_Available(my_item, available_quantity))

#         return render(request, 'item_list.html', {
#             'items_with_q': available_items,
#             'borrowed_item_records' : borrowed_item_records})
#     else:
#         return redirect(reverse_lazy('login'))

class ItemDetailView(DetailView):
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
    class Item_and_Quantity:
        def __init__(self, item, available_quantity):
            self.item = item
            self.available_quantity = available_quantity

    search_query = request.GET.get('search_query')
    
    item_containing_query = Item.objects.filter(
            Q(name__contains=search_query)
        )

    borrowed_item = Borrow.objects.filter(
            item_borrowed__in=item_containing_query
        ).values(
            'item_borrowed'
        ).annotate(
            Sum('quantity')
        )

    items_and_q = []

    for an_item in list(item_containing_query):
        # Don't display if this item belong to the user himself
        if request.user.is_authenticated:
            if an_item.owner == request.user:
                continue
        available_quantity = an_item.quantity
        # Get the amount available
        for a_borrowed_item in borrowed_item.values('item_borrowed_id', 'quantity__sum'):
            if a_borrowed_item['item_borrowed_id'] == an_item.id:
                available_quantity = an_item.quantity - a_borrowed_item['quantity__sum']
                break
        # Add to the list only if the item is available
        if (available_quantity > 0):
            items_and_q.append(Item_and_Quantity(an_item, available_quantity))

    return render(
        request,
        'item_search.html',
        {'items_and_q' : items_and_q, 'items_count' : len(items_and_q), 'query' : search_query})

def item_borrow_view(request, pk):
    
    if (not request.user.is_authenticated):
        return redirect(reverse_lazy('login'))

    item = Item.objects.get(pk = pk)
    if (request.user == item.owner):
        return HttpResponseForbidden()

    form = BorrowForm
    error_msg = None

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            new_borrow = Borrow(
                quantity=form.cleaned_data['quantity'], 
                return_date=form.cleaned_data['return_date'],
                borrower=request.user,
                item_borrowed=item,
            )
            
            available_quantity = item.quantity - Borrow.objects.filter(
                    item_borrowed=item
                ).aggregate(
                    total_borrowed=Coalesce(Sum('quantity'),0)
                )['total_borrowed']
            
            if (form.cleaned_data['quantity'] <= available_quantity):
                new_borrow.save()
                return redirect(reverse_lazy('items_list'))
            else:
                error_msg = 'You borrowed too much item'

    template_name = 'item_borrow.html'
    

    return render(request, template_name, {'form': form, 'item' : item, 'error_msg' : error_msg, 'item' : item})



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
