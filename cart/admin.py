from django.contrib import admin
from .models import *
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class CartItemInline(NestedStackedInline):
    model = CartItem
    extra = 0

class CartAdmin(NestedModelAdmin):
    model = Cart
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)