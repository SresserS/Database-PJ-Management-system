from django.contrib import admin
from django.urls import path,include
from startlib import views

urlpatterns = [
    path('add_books/',views.add_books),
    path('select_books/',views.select_books,name='select_books'),
    path('add_books/',views.add_books,name='add_books'),
    path('update_books/',views.update_books,name='update_books'),
    path('delete_books/',views.delete_books,name='delete_books'),
    path('inbooks/',views.inbooks,name='inbooks'),
    path('inbooks_pay/',views.inbooks_pay,name='inbooks_pay'),
    path('inbooks_cancel/',views.inbooks_cancel,name='inbooks_cancel'),
    path('select_inbooks/',views.select_inbooks,name='select_inbooks'),
    path('trans_income_to_books/',views.trans_income_to_books,name='trans_income_to_books'),
    path('add_sale/',views.add_sale,name='add_sale'),
    path('add_store/',views.add_store,name='add_store'),
    path('add_poss/',views.add_poss,name='add_poss'),
    path('select_finance/',views.select_finance,name='select_finance'),
    path('select_store/',views.select_store,name='select_store'),
    path('select_owner/',views.select_owner,name='select_owner'),
]
