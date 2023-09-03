from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


class CreateForm(APIView):
    def post(self,request):
        data = request.data
        CallbackForm.objects.create(**data)
        return Response(status=200)
