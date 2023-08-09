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
    # delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, blank=True, null=True)
    # delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.SET_NULL, blank=True, null=True)
    # payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, blank=True, null=True)
    # client = models.ForeignKey('client.Client', on_delete=models.CASCADE, blank=True, null=True)
    # manager = models.ForeignKey('user.User', on_delete=models.SET_NULL, blank=True, null=True)

    order_old_id = models.CharField(max_length=255,blank=True,null=True)
    order_old_data = models.TextField(blank=True,null=True)
    order_old_items = models.TextField(blank=True,null=True)
    order_old_payments = models.TextField(blank=True,null=True)

