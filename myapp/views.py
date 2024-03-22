from django.shortcuts import render, redirect
from django.db.models import Sum, F, Count, Subquery, OuterRef
from datetime import date
from . import forms
from . import models
from . import signals

# Create your views here.
def home(request):
    return render(request, 'home.html')

def add_medicine(request):
    if request.method == 'POST':
        form = forms.MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = forms.MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})

def add_store(request):
    if request.method == 'POST':
        form = forms.StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = forms.StoreForm()
    return render(request, 'add_store.html', {'form': form})

def add_dealer(request):
    if request.method == 'POST':
        form = forms.DealerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = forms.DealerForm()
    return render(request, 'add_dealer.html', {'form': form})

def add_purchase(request):
    if request.method == 'POST':
        form = forms.PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = forms.PurchaseForm()
    return render(request, 'add_purchase.html', {'form': form})

def add_customer(request):
    if request.method == 'POST':
        form = forms.CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = forms.CustomerForm()
    return render(request, 'add_customer.html', {'form': form})

def add_transaction(request):
    if request.method == 'POST':
        form = forms.TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = forms.TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})
        
def success(request):
    return render(request, 'success_page.html')

def show_medicines(request):
    medicines = models.Medicine.objects.all().order_by('med_id')  # Retrieve all Medicine objects
    return render(request, 'show_medicines.html', {'medicines': medicines})

def show_stores(request):
    stores = models.Store.objects.all().order_by('store_id')  # Retrieve all store objects
    return render(request, 'show_stores.html', {'stores': stores})

def show_dealers(request):
    dealers = models.Dealer.objects.all().order_by('dealer_id')  # Retrieve all dealer objects
    return render(request, 'show_dealers.html', {'dealers': dealers})

def show_purchases(request):
    purchases = models.Purchase.objects.all()  # Retrieve all purchase objects
    return render(request, 'show_purchases.html', {'purchases': purchases})

def show_customers(request):
    customers = models.Customer.objects.all().order_by('cust_id')  # Retrieve all customer objects
    return render(request, 'show_customers.html', {'customers': customers})

def show_transactions(request):
    transactions = models.Transaction.objects.all()  # Retrieve all transaction objects
    return render(request, 'show_transactions.html', {'transactions': transactions})

def show_quants(request):
    quants = models.Quant.objects.all().order_by('store_id')  # Retrieve all Medicine objects
    return render(request, 'show_quants.html', {'quants': quants})

def total_bills(request):
    total_bills = models.Transaction.objects.values('cust_id', 'store_id')\
                                        .annotate(total_bill=Sum('total'))\
                                        .values('bill_id', 'cust_id', 'store_id', 'total_bill')\
                                        .order_by('cust_id')
    return render(request, 'total_bills.html', { 'total_bills':total_bills })

def total_store_sale(request):
    # Perform a LEFT JOIN between Store and Transaction models
    total_sales = models.Store.objects.values('store_id', 'name')\
                                .annotate(total_sale=Sum('transaction__total'))\
                                .values('store_id', 'name', 'total_sale')\
                                .order_by('-total_sale')
    return render(request, 'total_store_sale.html', { 'total_sales': total_sales })

def unsold_medicine(request):
    unsold_medicines = models.Purchase.objects.annotate(
        total_quantity_sold=Subquery(
            models.Transaction.objects.filter(
                med_id=OuterRef('med_id'),
                store_id=OuterRef('store_id')
            ).values('med_id', 'store_id').annotate(
                total_quantity=Count('quantity')
            ).values('total_quantity')
        )
    ).filter(total_quantity_sold__isnull=True).values(
        'store_id', 'store_id__name', 'med_id', 'med_id__name', 'quantity_supplied')\
        .order_by('-quantity_supplied')
    return render(request, 'unsold_medicine.html', { 'unsold_medicines':unsold_medicines })

def find_sold_medicines(request):
    sold_medicines = models.Transaction.objects.values(
        'store_id', 'store_id__name', 'med_id', 'med_id__name'
    ).annotate(
        total_quantity_sold=Sum('quantity')
    )
    return render(request, 'sold_medicine.html', { 'sold_medicines':sold_medicines })

def most_sold_medicine_info(request):
    most_sold_medicines = models.Transaction.objects.select_related('med_id').values(
        'med_id', 'med_id__name', 'med_id__composition', 'med_id__mfg_date',
        'med_id__exp_date', 'med_id__cost_per_tab', 'med_id__mrp_per_tab'
    ).annotate(total_quantity=Sum('quantity'), total=Sum('total')
    ).order_by('-total_quantity')
    return render(request, 'most_sold_medicine.html', { 'most_sold_medicines':most_sold_medicines })

def get_expired_medicines(request):
    expired_medicines = models.Quant.objects.select_related('med_id').filter(
        med_id__exp_date__lt=date.today()
    ).order_by('med_id__med_id').values(
        'med_id', 'med_id__name', 'med_id__composition',
        'med_id__mfg_date', 'med_id__exp_date', 'med_id__cost_per_tab', 'med_id__mrp_per_tab',
        'store_id', 'quantity'
    )
    return render(request, 'get_expired_medicines.html', { 'expired_medicines':expired_medicines })

def get_unexpired_medicines(request):
    unexpired_medicines = models.Quant.objects.select_related('med_id').filter(
        med_id__exp_date__gt=date.today()
    ).order_by('med_id__med_id').values(
        'med_id', 'med_id__name', 'med_id__composition',
        'med_id__mfg_date', 'med_id__exp_date', 'med_id__cost_per_tab', 'med_id__mrp_per_tab',
        'store_id', 'quantity'
    )
    return render(request, 'get_unexpired_medicines.html', { 'unexpired_medicines':unexpired_medicines })

def get_transaction_profit(request):
    transaction_profits = models.Transaction.objects.values(
        'med_id', 'med_id__name', 'med_id__composition',
        'med_id__mfg_date', 'med_id__exp_date', 'med_id__cost_per_tab', 'med_id__mrp_per_tab'
    ).annotate(
        store_id=F('store_id'),  # Use F expression to prevent aggregation error
        quantity=F('quantity'),
        profit=Sum(F('total') - F('quantity') * F('med_id__cost_per_tab'))
    ).order_by('med_id')
    return render(request, 'transaction_profit.html', { 'transaction_profits':transaction_profits })

def get_manufacturer_profit(request):
    manufacturer_profits = models.Transaction.objects.values(
        'med_id__manufacturer'
    ).annotate(
        profit=Sum(F('total') - F('quantity') * F('med_id__cost_per_tab'))
    ).order_by('profit')
    return render(request, 'manufacturer_profit.html', { 'manufacturer_profits':manufacturer_profits })

def get_store_profit(request):
    store_profits = models.Transaction.objects.values(
        'store_id'
    ).annotate(
        profit=Sum(F('total') - F('quantity') * F('med_id__cost_per_tab'))
    ).values(
        'store_id', 'store_id__name', 'store_id__store_runner', 'profit'
    ).order_by('-profit')
    return render(request, 'store_profit.html', { 'store_profits':store_profits })