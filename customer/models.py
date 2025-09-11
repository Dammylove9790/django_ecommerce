from django.db import models
import uuid
from authentications import models as userauth_models
from store import models as store_models


# Create your models here.


DELIVERY_STATUS = (
    ('New Order' , 'New Order'),
    ('Proccessing' , 'Proccessing'),
    ('Order Shipped' , 'Order Shipped'),
    ('Delivered' , 'Delivered'),
)

class CustomerAddress(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    customer = models.ForeignKey(userauth_models.User, on_delete=models.CASCADE, related_name='customer_address')
    fullname = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Customer Addresses'
        ordering = ['-date']

    def __str__(self):
        return self.customer.username



class Whishlist(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True, )
    customer = models.ForeignKey(userauth_models.User, on_delete=models.CASCADE, related_name='customer_wishlist')
    product = models.ForeignKey(store_models.Product, related_name='product_in_wishlist', on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.product.name


class DeliveryNotification(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    customer = models.ForeignKey(userauth_models.User, on_delete=models.CASCADE, related_name='customer_delivery_notification')
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

