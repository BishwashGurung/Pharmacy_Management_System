from django import forms
from . import models

class MedicineForm(forms.ModelForm):
    class Meta:
        model = models.Medicine
        fields = ['med_id', 'name', 'composition', 'mfg_date', 'exp_date', 'cost_per_tab', 'mrp_per_tab', 'manufacturer']

class StoreForm(forms.ModelForm):
    class Meta:
        model = models.Store
        fields = ['store_id', 'name', 'address', 'contact', 'store_runner']

class DealerForm(forms.ModelForm):
    class Meta:
        model = models.Dealer
        fields = ['dealer_id', 'name', 'address', 'phone']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = models.Purchase
        fields = ['purchase_id', 'med_id', 'store_id', 'dealer_id', 'quantity_supplied']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['cust_id', 'name', 'address', 'phone']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['bill_id', 'cust_id', 'store_id', 'med_id', 'quantity', 'trans_date']