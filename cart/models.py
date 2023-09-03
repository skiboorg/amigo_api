from _decimal import Decimal

from django.db import models


class Cart(models.Model):
    sessionID = models.CharField(max_length=255, blank=True, null=True)
    totalPrice = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='products')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, blank=True, null=True)
    productPrice = models.ForeignKey('product.ProductPrice', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    totalPrice = models.DecimalField(default=0, decimal_places=2, max_digits=8, null=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.totalPrice = self.productPrice.cost * Decimal(self.amount)
    #     super().save(*args, **kwargs)


