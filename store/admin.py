from django.contrib import admin
from store.models import * 

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image',)
    list_editable = ('image',)
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)




class GalleryInline(admin.TabularInline):
    model = Gallery

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'regular_price', 'in_stock', 'product_status', 'featured',)
    search_fields = ('name', 'category__name',)
    inlines = (GalleryInline, ProductVariantInline)
    prepopulated_fields = {'slug' : ('name', 'uuid',)}
admin.site.register(Product, ProductAdmin)




class VariantOptionsInline(admin.TabularInline):
    model = VariantOptions

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name',)
    inlines = (VariantOptionsInline,)
admin.site.register(ProductVariant, ProductVariantAdmin)




admin.site.register(VariantOptions)
admin.site.register(Gallery)




class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'price', 'total', 'date', )
admin.site.register(Cart, CartAdmin)




class OrderItemsInline(admin.TabularInline):
    model = OrderItems

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','total','shipping_method','order_status','payment_method','payment_status','payment_id','date',)
    inlines = [OrderItemsInline,]
    # search_fields = ('',)
    # ordering = ('-date',)
admin.site.register(Order, OrderAdmin)




class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order','product','vendor','customer','color','size','price','quantity','total','shipping_method','order_status','date',)
    # ordering = ('-date',)
admin.site.register(OrderItems, OrderItemsAdmin)
