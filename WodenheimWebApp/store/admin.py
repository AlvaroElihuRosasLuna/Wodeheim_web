from django.contrib import admin

# Register your models here.

from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date_ordered', 'complete']
    list_filter = ['complete']
    inlines = [OrderItemInline]


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)