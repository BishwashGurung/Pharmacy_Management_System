from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Purchase, Medicine, Quant, Transaction

@receiver(pre_save, sender=Purchase)
def calculate_purchase_cost(sender, instance, **kwargs):
    """
    Signal handler to calculate purchase_cost before inserting Retail object.
    """
    with transaction.atomic():
        if not instance.purchase_cost:
            # Calculate purchase_cost only if it's not already set
            try:
                # Retrieve Medicine object corresponding to the Retail instance's med_id
                medicine_obj = Medicine.objects.get(med_id=instance.med_id.med_id)
                # Calculate purchase_cost based on quantity_supplied and cost_per_tab
                instance.purchase_cost = instance.quantity_supplied * medicine_obj.cost_per_tab
            except Medicine.DoesNotExist:
                # If Medicine object does not exist, set purchase_cost to None
                instance.purchase_cost = None

@receiver(post_save, sender=Purchase)
def handle_purchase_insert(sender, instance, **kwargs):
    """
    Signal handler to handle Purchase object insertion.
    """
    with transaction.atomic():
        try:
            # Attempt to retrieve a Quant object corresponding to the Purchase instance
            quant_obj = Quant.objects.get(med_id=instance.med_id.med_id, store_id=instance.store_id.store_id)
            # If the Quant object already exists, update its quantity
            quant_obj.quantity += instance.quantity_supplied
            quant_obj.save()
        except Quant.DoesNotExist:
            # If the Quant object does not exist, create a new one
            quant_obj = Quant.objects.create(
                med_id=instance.med_id,
                store_id=instance.store_id,
                quantity=instance.quantity_supplied
            )

@receiver(pre_save, sender=Transaction)
def check_medicine_available(sender, instance, **kwargs):
    """
    Signal handler to check if amount of medicine being purchased is available in the store before inserting Transaction object.
    """
    with transaction.atomic():
        try:
            quant_obj = Quant.objects.get(med_id=instance.med_id, store_id=instance.store_id)
            if quant_obj.quantity < instance.quantity:
                raise ValueError("Warning: Not sufficient medicine quantity in the store")
        except Quant.DoesNotExist:
            # Raise a warning indicating that the medicine is not available in the store
            raise ValueError("Warning: Medicine not available on store")
        
@receiver(pre_save, sender=Transaction)
def check_expired(sender, instance, **kwargs):
    """
    Signal handler to check for expired medicine before inserting Transaction object.
    """
    with transaction.atomic():
        # Retrieve the Medicine object corresponding to the Transaction instance's med_id
        try:
            medicine_obj = Medicine.objects.get(med_id=instance.med_id.med_id)
            # Check if the expiry date of the medicine is earlier than the purchase date
            if medicine_obj.exp_date < instance.trans_date:
                # Raise a warning indicating that the expiry date is earlier than the purchase date
                raise ValueError("Warning: expiry date < purchase date")
        except Medicine.DoesNotExist:
            # Handle the case where Medicine object does not exist
            raise ValueError("Medicine does not exist.")
        
@receiver(pre_save, sender=Transaction)
def calculate_total_amount(sender, instance, **kwargs):
    """
    Signal handler to calculate total amount before inserting Transaction object.
    """
    with transaction.atomic():
        # Retrieve the Medicine object corresponding to the Transaction instance's med_id
        try:
            medicine_obj = Medicine.objects.get(med_id=instance.med_id.med_id)
            # Calculate total amount based on quantity and mrp_per_tab
            total_amount = instance.quantity * medicine_obj.mrp_per_tab
            instance.total = total_amount
        except Medicine.DoesNotExist:
            # Handle the case where Medicine object does not exist
            raise ValueError("Medicine does not exist.")
        
@receiver(post_save, sender=Transaction)
def update_quant(sender, instance, **kwargs):
    """
    Signal handler to update QUANT after inserting Transaction object.
    """
    with transaction.atomic():
        # Retrieve Quant object corresponding to the Transaction instance's med_idand store_id
        try:
            quant_obj = Quant.objects.get(med_id=instance.med_id, store_id=instance.store_id)
            # Update the quantity in the Quant object
            quant_obj.quantity -= instance.quantity
            quant_obj.save()
        except Quant.DoesNotExist:
            # Handle the case where Quant object does not exist
            raise ValueError("Quant data doesnot exist for the given keys.")