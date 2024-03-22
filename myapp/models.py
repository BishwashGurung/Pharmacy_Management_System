from django.db import models

# Create your models here.

class Medicine(models.Model):
    med_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    composition = models.CharField(max_length=70)
    mfg_date = models.DateField()
    exp_date = models.DateField()
    cost_per_tab = models.IntegerField()
    mrp_per_tab = models.IntegerField()
    manufacturer = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(exp_date__lte='2030-01-01'), name='exp_date_check'),
            models.CheckConstraint(check=models.Q(mfg_date__gte='2018-01-01'), name='mfg_date_check')
        ]

class Store(models.Model):
    store_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=70)
    contact = models.CharField(max_length=25)
    store_runner = models.CharField(max_length=25)

class Dealer(models.Model):
    dealer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=70)
    phone = models.CharField(max_length=25)

class Purchase(models.Model):
    purchase_id = models.CharField(max_length=20, primary_key=True)
    med_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, to_field='med_id', related_name='purchase_med_id')
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, to_field='store_id')
    dealer_id = models.ForeignKey(Dealer, on_delete=models.CASCADE, to_field='dealer_id')
    quantity_supplied = models.IntegerField()
    purchase_cost = models.IntegerField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity_supplied__lte=500), name='quantity_supplied_check'),
            models.UniqueConstraint(fields=['purchase_id', 'med_id', 'store_id', 'dealer_id'], name='unique_retail_entry')
        ]

class Customer(models.Model):
    cust_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=70, blank=True, null=True)
    phone = models.CharField(max_length=15)

class Transaction(models.Model):
    bill_id = models.IntegerField()
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='cust_id')
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, to_field='store_id')
    med_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, to_field='med_id', related_name='transaction_med_id')
    quantity = models.IntegerField()
    trans_date = models.DateField()
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__lte=150), name='transaction_quantity_check'),
            models.CheckConstraint(check=models.Q(trans_date__lt='2030-01-01', trans_date__gt='2018-01-01'), name='transaction_date_check'),
            models.UniqueConstraint(fields=['bill_id', 'med_id'], name='unique_transaction_entry')
        ]

class Quant(models.Model):
    med_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, to_field='med_id', related_name='quant_med_id')
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, to_field='store_id')
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['med_id', 'store_id'], name='unique_quant_entry')
        ]