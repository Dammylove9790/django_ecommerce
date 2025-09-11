from django.contrib import admin
from vendor.models import VendorAddress, VendorPaymentDetails, VendorPayout, DeliveryNotification

# Register your models here.
class VendorAddressAdmin(admin.ModelAdmin):
    pass
admin.site.register(VendorAddress, VendorAddressAdmin)



class VendorPaymentDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(VendorPaymentDetails, VendorPaymentDetailsAdmin)



class VendorPayoutAdmin(admin.ModelAdmin):
    pass
admin.site.register(VendorPayout, VendorPayoutAdmin)



class DeliveryNotificationAdmin(admin.ModelAdmin):
    pass
admin.site.register(DeliveryNotification, DeliveryNotificationAdmin)
