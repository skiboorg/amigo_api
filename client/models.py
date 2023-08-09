from django.db import models


class Category(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class Status(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class Client(models.Model):
    manager = models.ForeignKey('user.User', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ManyToManyField(Category, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey('data.City', on_delete=models.SET_NULL, blank=True, null=True)
    fio = models.CharField('ФИО', max_length=255, blank=False, null=True)
    web = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField('Адрес', blank=True, null=True)
    comment = models.TextField('КОММЕНТАРИЙ',blank=True, null=True)
    created_at = models.DateField(null=True)

    def __str__(self):
        return f'{self.fio}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Contact(models.Model):
    name = models.CharField('ИМЯ', max_length=255, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=255, blank=True, null=True)
    email = models.CharField('Email', max_length=255, blank=True, null=True)
    invite = models.CharField('Приглашение', max_length=255, blank=True, null=True)
    comment = models.TextField('КОММЕНТАРИЙ',blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='contacts')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Контакт клиента'
        verbose_name_plural = 'Контакты клиента'


class Contractor(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    inn = models.CharField('Инн', max_length=255, blank=False, null=True)
    is_physic = models.BooleanField('Физ. лицо?', blank=False, null=True)
    is_base = models.BooleanField('Базовый ?', blank=False, null=True)
    comment = models.TextField('КОММЕНТАРИЙ',blank=True, null=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='contractors')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Плательщики'
        verbose_name_plural = 'Плательщики'


class DeliveryAddress(models.Model):
    old_city = models.CharField('Город в старой базе', max_length=255, blank=True, null=True)
    city = models.ForeignKey('data.City', on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField('Адрес', max_length=255, blank=True, null=True)
    flat = models.CharField('Офис/квартира', max_length=255, blank=True, null=True)
    comment = models.TextField('Дополнительно', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='delivery_addresses')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адрес доставки'


class Note(models.Model):
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    is_done = models.BooleanField('Выполнена?', blank=False, null=True)
    by_shedule = models.BooleanField('Расписание ?', blank=False, null=True)
    priority = models.BooleanField('Расписание ?', blank=False, null=True)
    note_old_type = models.CharField('Тип из старой базы', max_length=255, blank=True, null=True)
    text = models.TextField('Текст',blank=True, null=True)
    created_at = models.DateTimeField(blank=True,null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='notes')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Заметки'
        verbose_name_plural = 'Заметки'


