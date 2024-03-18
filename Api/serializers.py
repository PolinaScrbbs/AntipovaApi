from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, Advertisement

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'phone_number']

        # Дополнительные параметры
        extra_kwargs = {
            'password': {'write_only': True},  #Пароль только для чтения
        }

    #Хеширование пароля
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super(UserSerializer, self).create(validated_data)
        Token.objects.create(user=user)
        return user
    
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['author', 'title', 'content', 'price', 'item_count', 'created_at', 'number_of_views']
