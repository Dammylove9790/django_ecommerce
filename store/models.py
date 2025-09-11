from django.db import models
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
# import shortuuid
import uuid

from authentications import models as userauth_model
import random



# Create your models here.

# product status
PRODUCT_STATUS = (
    ('Published', 'Published'),
    ('Draft', 'Draft'),
    ('Disabled', 'Disabled'),
)

PAYMENT_STATUS = (
    ('Paid', 'Paid'),
    ('Proccessing', 'Proccessing'),
    ('Failed', 'Failed'),
)

PAYMENT_METHOD = (
    ('Paypal', 'Paypal'),
    ('Flutterwave', 'Flutterwave'),
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

RATING = (
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****'),
)




class Category(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name} : {self.slug}'

    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
       if not self.slug:
           self.slug = slugify(self.name)
       super(Category, self).save(*args, **kwargs) # Call the real save() method




class Product(models.Model):
    uuid = ShortUUIDField(unique=True, editable=True, length=10, max_length=40, prefix='', alphabet='abcdefghij123456')
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    description = models.TextField(max_length=1000,blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='product_category')

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True, verbose_name='Selling Price')
    regular_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True, verbose_name='Regular Price')
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True, verbose_name='Shipping Amount')

    in_stock = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Products in Stock')

    product_status = models.CharField(max_length=255, choices=PRODUCT_STATUS, blank=True, null=True)
    featured = models.BooleanField(default=0, blank=True, null=True)

    vendor = models.ForeignKey(userauth_model.User, related_name='vendor_product', on_delete=models.SET_NULL, blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-id']

    def product_gallery(self):
        return Gallery.objects.filter(product=self)
    
    def product_variant(self):
        return ProductVariant.objects.filter(Product=self)


    def save(self, *args, **kwargs):
       if not self.slug:
           self.slug = slugify(self.name) + '-' + str(random.randint(10,50)*random.randint(10,50)*random.randint(10,50))
       super(Product, self).save(*args, **kwargs) # Call the real save() method



# product variants can be size, color and more
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant')
    name = models.CharField(max_length=255, blank=True, null=True)

    def variant_options(self):
        return VariantOptions.objects.filter(variant=self)
    
    class Meta:
        verbose_name_plural = 'Product Variants'
    
    def __str__(self):
        return self.name



# variant options can be different sizes under the size, color options and more 
class VariantOptions(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='variant_options')
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Variant Options'
        



class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_gallery')
    image = models.ImageField(upload_to='image', default='default-product-image.jpg')

    def __str__(self):
        return f'{self.product.name.title()} image'
    
    class Meta:
        verbose_name_plural = 'Gallery'



class Cart(models.Model):
    uuid = ShortUUIDField(unique=True, editable=True, length=10, max_length=40, prefix='', alphabet='abcdefghij123456')
    customer = models.ForeignKey(userauth_model.User, related_name='customer_cart', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} is in the cart'



class Order(models.Model):
    uuid = ShortUUIDField(unique=True, editable=True, length=10, max_length=40, prefix='', alphabet='abcdefghij123456')
    vendor = models.ManyToManyField(userauth_model.User, related_name='vendor_order', blank=True)
    customer = models.ForeignKey(userauth_model.User, related_name='customer_order', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    shipping_method = models.CharField(max_length=255, choices=SHIPPING_SERVICE, blank=True, null=True)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS, default='Pending', blank=True, null=True)
    order_address = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD, blank=True, null=True)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS, default='Proccessing', blank=True, null=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.username
    
    def order_items(self):
        return OrderItems.objects.filter(order=self)
    
    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ['-date']




class OrderItems(models.Model):
    uuid = ShortUUIDField(unique=True, editable=True, length=10, max_length=40, prefix='', alphabet='abcdefghij123456')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(userauth_model.User, related_name='vendor_orderitems', on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(userauth_model.User, related_name='customer_orderitems', on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    shipping_method = models.CharField(max_length=255, choices=SHIPPING_SERVICE, blank=True, null=True)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS, default='Pending', blank=True, null=True)
    order_address = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Order Items'
        ordering = ['-date']

    def __str__(self):
        return self.order

