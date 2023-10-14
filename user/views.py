import json

import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from rest_framework import filters

import logging
logger = logging.getLogger(__name__)



class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AddUser(APIView):
    def post(self,request):
        print(request.data)
        data = request.data
        result = {}

        if data['password1'] != data['password2']:
            result = {'success':False,'message':'Пароли не совпадают'}
            return Response(result,status=200)
        new_user = User.objects.create(
            email=data['email'],
            client_id=data['client'],
            login=data['email'],
            fio=data['fio'],
            comment=data['comment'],
            is_manager=data['is_manager'],
            is_staff=data['is_staff'],
            plain_password=data['password1'],
        )
        new_user.set_password(data['password1'])
        new_user.save()
        result = {'success': True, 'message': 'Пользователь успешно создан'}
        return Response(result, status=200)



class UpdateUser(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        setattr(request.data, '_mutable', True)
        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        # try:
        #     user_networks = request.data.pop('networks')
        # except:
        #     user_networks = []


        data = json.loads(json.dumps(request.data))



        json_data = {}
        for dat in data:
            json_data[dat] = json.loads(data[dat])
        instance = User.objects.get(uuid=json_data['uuid'])


        serializer = UserSerializer(instance,data=json_data)

        if serializer.is_valid():
            obj = serializer.save()
            obj.added_by = request.user
            obj.save()
            # for index,file in enumerate(request.FILES.getlist('files')):
            #     UserFile.objects.create(file=file,user=obj,description=files_descriptions[index])
            #
            # for network in user_networks:
            #     network_json_data = json.loads(network)
            #     print(network_json_data)
            #
            #     UserNetwork.objects.create(user=obj,name=network_json_data['name'],link=network_json_data['link'])

        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

class GetMyUsers(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.get(uuid=self.request.query_params.get('id'))
        return User.objects.filter(added_by=user)


class GetUserByUuid(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'



class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'



class UserPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 10000


class UserFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="Search")
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(client__fio__icontains=value) |
            Q(fio__icontains=value)

        )
    class Meta:
        model = User
        fields = ['is_manager','is_staff']

class GetAllUsers(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = UserFilter

class GetRoles(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

class GetManagers(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_manager=True)

class GetUserByRole(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(role__id = self.request.query_params.get('id'))




