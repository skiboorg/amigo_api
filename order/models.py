from django.db import models

class Delivery(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class DeliveryCompany(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class PaymentType(models.Model):
    name = models.CharField('НАЗВАНИЕ', max_length=255, blank=False, null=True)
    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    session_id = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    userName = models.CharField(max_length=255, blank=True, null=True)
    orderComment = models.TextField(blank=True, null=True)

    totalPrice = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)

    order_old_id = models.CharField(max_length=255,blank=True,null=True)
    order_old_data = models.TextField(blank=True,null=True)
    order_old_items = models.TextField(blank=True,null=True)
    order_old_payments = models.TextField(blank=True,null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='products')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, blank=True, null=True)
    productPrice = models.ForeignKey('product.ProductPrice', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    totalPrice = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)

