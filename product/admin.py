from django.contrib import admin
from django.utils.safestring import mark_safe
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import *

class ProductPriceInline(NestedStackedInline):
    model = ProductPrice
    extra = 0


class ProductGalleryImageInline(NestedStackedInline):
    model = ProductGalleryImage
    extra = 0
    readonly_fields = ['image_preview']

    def image_preview(self, obj):

        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return 'Нет изображения'

    image_preview.short_description = 'Текущее изображение'



class ProductAdmin(NestedModelAdmin):
    model = Product
    list_display = ('image_preview','name',)
    readonly_fields = ['image_preview']
    inlines = [ProductGalleryImageInline, ProductPriceInline]
    fields = [
        'image_preview',
        'category',
        'filters',
        'isActive',
        'isNew',
        'isDiscount',
        'discount',
        'isPromotionActive',
        'promotionText',
        'vendorCode',
        'name',
        'slug',
        'shortDescription',

        'description',
        'feedingRate',
        'delivery',
    ]
    def image_preview(self, obj):
        if obj.gallery.all().filter(is_main=True):
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.gallery.all().filter(is_main=True).first().image.url))
        else:
            return 'Нет изображения'

    image_preview.short_description = 'Текущее изображение'


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Filter)
admin.site.register(Sale)
