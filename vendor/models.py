from django.db import models

import uuid
from authentications import models as userauth_models
from store import models as store_models

# Create your models here.

PAYMENT_STATUS = (
    ('Paid', 'Paid'),
    ('Proccessing', 'Proccessing'),
    ('Failed', 'Failed'),
)

PAYMENT_METHOD = (
    ('Nigeria Banks', 'Nigeria Banks'),
    ('Flutterwave', 'Flutterwave'),
    ('Paypal', 'Paypal'),
)

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Proccessing', 'Proccessing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

SHIPPING_SERVICE = (
    ('Car', 'Car'),
    ('Bike', 'Bike'),
    ('Air', 'Air'),
)

DELIVERY_STATUS = (
    ('New Order' , 'New Order'),
    ('Proccessing' , 'Proccessing'),
    ('Order Shipped' , 'Order Shipped'),
    ('Delivered' , 'Delivered'),
)




class VendorAddress(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    vendor = models.OneToOneField(userauth_models.User, on_delete=models.CASCADE, related_name='vendor_address')
    store_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Vendor Address'
        ordering = ['vendor']

    def __str__(self):
        return self.vendor.username




class VendorPaymentDetails(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    vendor = models.ForeignKey(userauth_models.User, on_delete=models.CASCADE, related_name='vendor_payment_details')

    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD, blank=True, null=True)

    # for Nigerian account
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    bank_code = models.CharField(max_length=255, blank=True, null=True)

    paypal_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Vendor Payment Details'
        
    def __str__(self):
        return self.bank_name 




class VendorPayout(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    vendor = models.ForeignKey(userauth_models.User, on_delete=models.CASCADE, related_name='vendor_payout')
    order_item = models.ForeignKey(store_models.OrderItems, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS, blank=True, null=True)
    payout_status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.vendor



class DeliveryNotification(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    vendor = models.ForeignKey(userauth_models.User, on_delete=models.CASCADE, related_name='vendor_delivery_notification')
    order = models.ForeignKey(store_models.Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=DELIVERY_STATUS, default=None, blank=True, null=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        result = ''
        if self.status == 'New Order':
            result = 'is a'
        elif self.status == 'Proccessing':
            result = 'is under'
        else :
            result = 'has been'
        return f'Order made on {self.date} {result} {self.status}'

