from django.db import models
from django_resized import ResizedImageField
from pytils.translit import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files import File
from django.db.models.signals import post_save


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

class Filter(models.Model):
    categories = models.ManyToManyField(ProductCategory, blank=False, related_name='filters')
    name = models.CharField('Название', max_length=255, blank=False, null=False)
    slug = models.CharField('ЧПУ', max_length=255,
                            help_text='Если не заполнено, создается на основе поля Назавание',
                            blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        #ordering = ('order_num',)
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    isAvailable = models.BooleanField('В наличии?', default=True)
    isActive = models.BooleanField('Отображать?', default=True)
    isNew = models.BooleanField('Товар новинка?', default=False)
    isDiscount = models.BooleanField('Товар со скидкой?', default=True)
    isPromotionActive = models.BooleanField('Отображать акционный блок?', default=False)
    promotionText = models.CharField('Текст в акционном блоке', max_length=255, blank=True, null=True)
    vendorCode = models.CharField('Артикул', max_length=255, blank=False, null=True)
    name = models.CharField('Название', max_length=255, blank=False, null=True)

    slug = models.CharField('ЧПУ',max_length=255,
                                 help_text='Если не заполнено, создается на основе поля Назавание',
                                 blank=True, null=True)

    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=False, null=True)
    filters = models.ManyToManyField(Filter, blank=False)
    shortDescription = models.TextField('Короткое описание', blank=True, null=True)
    discount = models.IntegerField('Скидка %', default=0, null=False)
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

class ProductTab(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='tabs')
    label = models.CharField('Название таба', max_length=255, blank=False, null=True)
    text = RichTextUploadingField('Текст', blank=True, null=True)

    def __str__(self):
        return f'{self.label}'

    class Meta:
        verbose_name = 'Таб товара'
        verbose_name_plural = 'Табы товаров'

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
    vendorCode = models.CharField('Артикул', max_length=255, blank=False, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='prices')
    weight = models.DecimalField('Вес, кг', decimal_places=3,max_digits=6, default=0, null=True)
    volume = models.DecimalField('Объем, m3', decimal_places=3,max_digits=6, default=0, null=True)
    textLabel = models.CharField('Фасовка',max_length=20, blank=False, null=True)
    price = models.DecimalField('Стоимость',decimal_places=2, max_digits=8, default=0, null=True)
    at_store = models.IntegerField('Остаток',default=0, null=True)
    isActive = models.BooleanField('Отображать?', default=True)

    def __str__(self):
        return f'{self.textLabel} - {self.price}'

    class Meta:
        ordering = ('product',)
        verbose_name = 'Цена/Вес товара'
        verbose_name_plural = 'Цены/Веса товаров'


class Sale(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)

    slug = models.CharField('ЧПУ', max_length=255,
                            help_text='Если не заполнено, создается на основе поля Назавание',
                            blank=True, null=True)
    description = RichTextUploadingField('Описание', blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    discount = models.IntegerField('Скидка %', default=0, null=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        #ordering = ('order_num',)
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def sale_post_save(sender, instance, created, **kwargs):
    for product in instance.products.all():
        product.isDiscount = True
        product.discount = instance.discount
        product.save()


post_save.connect(sale_post_save, sender=Sale)


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='feedbacks')
    text = RichTextUploadingField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return f'От {self.name}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'



class FeedbackImage(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='images')
    image = ResizedImageField(size=[120, 200], quality=95, force_format='WEBP', upload_to='fb/gallery',
                              blank=False, null=True)

    def __str__(self):
        return f''


    class Meta:
        verbose_name = 'Картинка отзыва'
        verbose_name_plural = 'Картинки отзывов'