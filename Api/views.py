from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .functions import get_user_by_token

#Получение и добавление пользователей
class UsersView(ListCreateAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response({"Users": serializer.data})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Создан пользователь": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Авторизация и создание токена
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)

#Получение списка объявлений и создание объявления    
class AdvertisementsView(ListCreateAPIView):
    serializer_class =  AdvertisementSerializer

    #Получение списка
    def get(self, request):
        token = request.GET.get('token', None)
        user = get_user_by_token(token)
        if not user:
            return Response({"error": f"Ошибка авторизации: {token} не найден"})
        advertisements = Advertisement.objects.all()
        serializer = self.serializer_class(advertisements, many=True)
        return Response({"Объявления": serializer.data})
    
    #Создание объявления
    def post(self, request):
        token = request.GET.get('token', None)
        user = get_user_by_token(token)
        if not user:
            return Response({"error": "Пользователь не найден"})
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({f"Объявление создано": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Работа с отдельными объявлениями   
class AdvertisementView(RetrieveUpdateDestroyAPIView):
    serializer_class =  AdvertisementSerializer
    
    #Получение объявления
    def get(self, request, **kwargs):
        token = request.GET.get('token', None)
        user = get_user_by_token(token)
        if not user:
            return Response({"error": "Пользователь не найден"})
        advertisement_id = request.data.get('id', None)
        if not advertisement_id:
            return Response({"error": "Id объявления не был получен"})
        try:
            advertisement = Advertisement.objects.get(id=advertisement_id)
            serializer = self.serializer_class(advertisement)
            return Response({"Advertisement": serializer.data})
        except Advertisement.DoesNotExist:
            return Response({"error": "Объявление не найдено"})
    
    #Обновление объявления
    def put(self, request):
        token = request.GET.get('token', None)
        user = get_user_by_token(token)
        if not user:
            return Response({"error": "Пользователь не найден"})
        advertisement_id = request.data.get('id', None)
        if not advertisement_id:
            return Response({"error": "Id объявления не был получен"})
        try:
            advertisement = Advertisement.objects.get(id=advertisement_id)
            serializer = self.serializer_class(advertisement, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({f"Объявление обновлено": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Advertisement.DoesNotExist:
            return Response({"error": "Объявление не найдено"})

    #Удаление объявления   
    def delete(self, request):
        token = request.GET.get('token', None)
        user = get_user_by_token(token)
        if not user:
            return Response({"error": "Пользователь не найден"})
        advertisement_id = request.data.get('id', None)
        if not advertisement_id:
            return Response({"error": "Id объявления не был получен"})
        try:
            advertisement = Advertisement.objects.get(id=advertisement_id) 
            advertisement.delete()
            return Response({"error": "Объявление удалено"})
        except Advertisement.DoesNotExist:
            return Response({"error": "Объявление не найдено"})
