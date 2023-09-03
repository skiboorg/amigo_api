from django.db import models
from django_resized import ResizedImageField
from pytils.translit import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files import File



class ProductCategory(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=False)
    image = ResizedImageField(size=[420, 420], quality=95, force_format='WEBP', upload_to='product/gallery',
                              blank=False, null=True)
    slug = models.CharField('ЧПУ', max_length=255,
                            help_text='Если не заполнено, создается на основе поля Назавание',
                            blank=True, null=True)
    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        #ordering = ('order_num',)
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

class ProductSubCategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=False, null=True, related_name='sub_categories')
    name = models.CharField('Название', max_length=255, blank=False, null=False)
    slug = models.CharField('ЧПУ', max_length=255,
                            help_text='Если не заполнено, создается на основе поля Назавание',
                            blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        #ordering = ('order_num',)
        verbose_name = 'Подкатегория товара'
        verbose_name_plural = 'Подкатегория товаров'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    isActive = models.BooleanField('Отображать?', default=True)
    isPromotionActive = models.BooleanField('Отображать акционный блок?', default=False)
    promotionText = models.CharField('Текст в акционном блоке', max_length=255, blank=True, null=True)
    vendorCode = models.CharField('Артикул', max_length=255, blank=False, null=True)
    name = models.CharField('Название', max_length=255, blank=False, null=True)

    slug = models.CharField('ЧПУ',max_length=255,
                                 help_text='Если не заполнено, создается на основе поля Назавание',
                                 blank=True, null=True)

    subCategory = models.ManyToManyField(ProductSubCategory, blank=True)
    shortDescription = models.TextField('Короткое описание', blank=True, null=True)
    description = RichTextUploadingField('Состав', blank=True, null=True)
    feedingRate = RichTextUploadingField('Норма кормления  ', blank=True, null=True)
    delivery = RichTextUploadingField('Доставка и оплата', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        #ordering = ('order_num',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductGalleryImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='gallery')
    image = ResizedImageField(size=[420, 420], quality=95, force_format='WEBP', upload_to='product/gallery',
                              blank=False, null=True)
    imageThumb = models.ImageField(upload_to='product/gallery/', blank=True, null=True, editable=False)
    is_main = models.BooleanField('Основная картинка', default=False)

    def __str__(self):
        return f''

    def save(self, *args, **kwargs):
        from .services import create_thumb
        if not self.imageThumb:
            self.imageThumb.save(f'{self.product.slug}-thumb.jpg', File(create_thumb(self.image)), save=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('is_main',)
        verbose_name = 'Картинка товара'
        verbose_name_plural = 'Картинки товаров'


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='prices')
    weight = models.DecimalField('Вес, кг', decimal_places=3,max_digits=6, default=0, null=True)
    textLabel = models.CharField('Название',max_length=20, blank=False, null=True)
    cost = models.DecimalField('Стоимость',decimal_places=2, max_digits=8, default=0, null=True)

    def __str__(self):
        return f'{self.textLabel} - {self.cost}'

    class Meta:
        verbose_name = 'Цена/Вес товара'
        verbose_name_plural = 'Цены/Веса товаров'