from django.db import models

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
