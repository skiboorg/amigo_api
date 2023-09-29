from _decimal import Decimal

from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

def calcCart(cart):
    totalPrice = 0
    for product in cart.products.all():
        totalPrice += Decimal(product.totalPrice)
    cart.totalPrice = totalPrice
    cart.save()
    return

class UpdateCart(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        session_id = data['session_id']
        # cart = Cart.objects.get(sessionID=session_id)
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            cart, _ = Cart.objects.get_or_create(sessionID=session_id)
        if data['action'] == 'add_amount':
            cartItem, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=data['product_id'],
                productPrice_id=data['productPrice_id']
            )
            print(cartItem)
            if created:
                cartItem.amount = 1
            else:
                cartItem.amount += 1
            cartItem.totalPrice = cartItem.amount * cartItem.productPrice.cost
            cartItem.save()
            calcCart(cart)
        if data['action'] == 'remove_amount':
            cartItem = CartItem.objects.get(
                cart=cart,
                product_id=data['product_id'],
                productPrice_id=data['productPrice_id']
            )
            if cartItem.amount - 1 == 0:
                cartItem.delete()
            else:
                cartItem.amount -= 1
                cartItem.totalPrice = cartItem.amount * cartItem.productPrice.cost
                cartItem.save()
            calcCart(cart)
        if data['action'] == 'delete_product':
            cartItem = CartItem.objects.get(
                cart=cart,
                product_id=data['product_id'],
                productPrice_id=data['productPrice_id']
            )

            cartItem.delete()
            calcCart(cart)

        return Response(status=200)


class GetCart(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        session_id = self.kwargs.get('session_id', None)
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
        else:
            cart, _ = Cart.objects.get_or_create(sessionID=session_id)
        return cart



