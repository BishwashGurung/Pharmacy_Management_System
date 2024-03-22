from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add_medicine/', views.add_medicine, name="add_medicine"),
    path('add_store/', views.add_store, name="add_store"),
    path('add_dealer/', views.add_dealer, name="add_dealer"),
    path('add_purchase/', views.add_purchase, name="add_purchase"),
    path('add_customer/', views.add_customer, name="add_customer"),
    path('add_transaction/', views.add_transaction, name="add_transaction"),
    path('success/', views.success, name="success_page"),
    path('show_medicines/', views.show_medicines, name="show_medicines"),
    path('show_stores/', views.show_stores, name="show_stores"),
    path('show_dealers/', views.show_dealers, name="show_dealers"),
    path('show_purchases/', views.show_purchases, name="show_purchases"),
    path('show_customers/', views.show_customers, name="show_customers"),
    path('show_transactions/', views.show_transactions, name="show_transactions"),
    path('show_quants/', views.show_quants, name="show_quants"),
    path('total_bills/', views.total_bills, name="total_bills"),
    path('total_store_sale/', views.total_store_sale, name="total_store_sale"),
    path('unsold_medicine/', views.unsold_medicine, name="unsold_medicine"),
    path('sold_medicine/', views.find_sold_medicines, name="sold_medicine"),
    path('most_sold_medicine/', views.most_sold_medicine_info, name="most_sold_medicine"),
    path('expired_medicines/', views.get_expired_medicines, name="expired_medicines"),
    path('unexpired_medicines/', views.get_unexpired_medicines, name="unexpired_medicines"),
    path('transaction_profit/', views.get_transaction_profit, name="transaction_profit"),
    path('manufacturer_profit/', views.get_manufacturer_profit, name="manufacturer_profit"),
    path('store_profit/', views.get_store_profit, name="store_profit")
]

