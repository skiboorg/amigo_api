from django.contrib import admin
from .models import *

class OrderItemInline (admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]

admin.site.register(Order,OrderAdmin)
admin.site.register(Delivery)
admin.site.register(DeliveryCompany)
admin.site.register(PaymentType)
admin.site.register(Status)