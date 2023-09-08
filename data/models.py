from django.db import models
from django_resized import ResizedImageField
from pytils.translit import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class City(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    timezone = models.CharField('Зона', max_length=255, blank=False, null=True)
    country = models.CharField('Страна', max_length=255, blank=False, null=True)
    post_index = models.CharField('Индекс', max_length=255, blank=False, null=True)
    region = models.CharField('Регион', max_length=255, blank=False, null=True)
    area = models.CharField('Область', max_length=255, blank=False, null=True)
    type = models.CharField('Тип', max_length=255, blank=False, null=True)
    latitude = models.CharField('Широта', max_length=255, blank=False, null=True)
    longtitude = models.CharField('Долгота', max_length=255, blank=False, null=True)

    def __str__(self):
        return f'{self.name}'

class BlogCategory(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # ordering = ('order_num',)
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogItem(models.Model):
    category = models.ForeignKey(BlogCategory,on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    shortDescription = models.TextField('Короткое описание', blank=True, null=True)
    description = RichTextUploadingField('Контент', blank=True, null=True)
    image = ResizedImageField(size=[800, 450], quality=95, force_format='WEBP', upload_to='blog',
                              blank=False, null=True)
    is_news_item = models.BooleanField('Это новость?',default=True, null=False)
    readTime = models.CharField('Время прочтения', max_length=255, blank=True, null=True)
    createdAt = models.DateField('Дата', blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)