from django.contrib import admin
from customer.models import CustomerAddress, DeliveryNotification, Whishlist


# Register your models here.
class  CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ('customer','fullname','mobile','country','state',)   #can either be a list or turple
admin.site.register( CustomerAddress,  CustomerAddressAdmin)

class  WhishlistAdmin(admin.ModelAdmin):
    list_display = ('customer','product',)   #can either be a list or turple
admin.site.register( Whishlist,  WhishlistAdmin)


class  DeliveryNotificationAdmin(admin.ModelAdmin):
    list_display = ('customer','status',)   #can either be a list or turple
admin.site.register( DeliveryNotification,  DeliveryNotificationAdmin)

