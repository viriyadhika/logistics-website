from django.urls import path
from .views import (
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemUpdateView,
    my_item_list,
    item_search_view,
    item_borrowed_view,
    ItemReturnView,
    item_borrow_view
)

urlpatterns = [
    path('', my_item_list, name='items_list'),
    path('new/', ItemCreateView.as_view(), name='item_new'),
    path('<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('search/', item_search_view, name='item_search_result'),
    path('<int:pk>/borrow', item_borrow_view, name='item_borrow'),
    path('borrowed/', item_borrowed_view, name='item_borrowed'),
    path('borrow_record/<int:pk>/return', ItemReturnView.as_view(), name='item_return')
]

