from _decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django_resized import ResizedImageField


class Delivery(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    image = ResizedImageField(size=[400, 300], quality=95, force_format='WEBP', upload_to='order/delivery',
                              blank=True, null=True)
    is_self_delivery = models.BooleanField(default=False, null=False)
    def __str__(self):
        return f'{self.name}'

class DeliveryCompany(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class PaymentType(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.name}'

class Status(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class DeliveryStatus(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    old_id = models.IntegerField(blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    track_code = models.CharField(max_length=255, blank=True, null=True)
    manager = models.ForeignKey('user.User', on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey('data.City',on_delete=models.SET_NULL,blank=True, null=True)
    client = models.ForeignKey('client.Client',on_delete=models.CASCADE,blank=True, null=True,related_name='orders')
    contractor = models.ForeignKey('client.Contractor',on_delete=models.SET_NULL,blank=True, null=True)
    contact = models.ForeignKey('client.Contact',on_delete=models.SET_NULL,blank=True, null=True)
    delivery = models.ForeignKey(Delivery,on_delete=models.SET_NULL,blank=True, null=True)
    delivery_price = models.DecimalField(default=0,decimal_places=2, max_digits=6,blank=True, null=True)
    delivery_company = models.ForeignKey(DeliveryCompany,on_delete=models.SET_NULL,blank=True, null=True)
    payment_type = models.ForeignKey(PaymentType,on_delete=models.SET_NULL,blank=True, null=True)
    status = models.ForeignKey(Status,on_delete=models.SET_NULL,blank=True, null=True)
    delivery_status = models.ForeignKey(DeliveryStatus,on_delete=models.SET_NULL,blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    delivery_comment = models.TextField(blank=True, null=True)
    is_archive = models.BooleanField(default=False, null=False)
    created_at_time = models.TimeField(auto_now_add=True, null=True)
    created_at_date = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)
    orderComment = models.TextField(blank=True, null=True)
    total_weight = models.DecimalField('Общий Вес, кг', decimal_places=3, max_digits=9, default=0, null=True)
    total_volume = models.DecimalField('Общий Объем, m3', decimal_places=3, max_digits=9, default=0, null=True)
    amount = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField('Общий Стоимость', decimal_places=2, max_digits=16, default=0, null=True)

    order_old_id = models.CharField(max_length=255,blank=True,null=True)
    order_old_data = models.TextField(blank=True,null=True)
    order_old_items = models.TextField(blank=True,null=True)
    order_old_payments = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ('-id',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='products')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, blank=True, null=True)
    productPrice = models.ForeignKey('product.ProductPrice', on_delete=models.CASCADE, blank=True, null=True)
    price_with_discount = models.DecimalField('Стоимость со скидкой', decimal_places=2, max_digits=8, default=0,
                                              null=True)
    total_weight = models.DecimalField('Общий Вес, кг', decimal_places=3, max_digits=9, default=0, null=True)
    total_volume = models.DecimalField('Общий Объем, m3', decimal_places=3, max_digits=9, default=0, null=True)
    amount = models.IntegerField(default=1,blank=True, null=True)
    total_price = models.DecimalField('Общий Стоимость', decimal_places=2, max_digits=13, default=0, null=True)

    class Meta:
        ordering = ('-id',)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.total_weight = self.productPrice.weight * Decimal(self.amount)
    #     self.total_volume = self.productPrice.volume * Decimal(self.amount)
    #     self.total_price = self.productPrice.price * Decimal(self.amount)
    #     super().save(*args, **kwargs)


def order_item_post_save(sender, instance, created, **kwargs):
    if created:
        instance.price_with_discount = instance.productPrice.price
        instance.save()
    # instance.total_weight = instance.productPrice.weight * Decimal(instance.amount)
    # instance.total_volume = instance.productPrice.volume * Decimal(instance.amount)
    # instance.total_price = instance.productPrice.price * Decimal(instance.amount)
    # print('save')

# def order_post_save(sender, instance, created, **kwargs):
#     for product in instance.products.all():
#         product.total_weight = product.productPrice.weight * Decimal(product.amount)
#         product.total_volume = product.productPrice.volume * Decimal(product.amount)
#         product.total_price = product.productPrice.price * Decimal(product.amount)
#         product.save()


#post_save.connect(order_post_save, sender=Order)
post_save.connect(order_item_post_save, sender=OrderItem)