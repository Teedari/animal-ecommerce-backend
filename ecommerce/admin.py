from django.contrib import admin

# Register your models here.

from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(DeliveryPoint)
admin.site.register(ProductImage)
