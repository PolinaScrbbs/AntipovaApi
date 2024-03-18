from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=50, unique=True, null=False, verbose_name='Email')
    password = models.CharField(max_length=30, null=False, verbose_name='Пароль')
    full_name = models.CharField(max_length=70, null=False, verbose_name='ФИО')
    phone_number = models.CharField(max_length=20, null=True, unique=True, verbose_name='Номер телефона')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name

class Advertisement(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Создатель объявления')
    title = models.CharField(max_length=50, null=False, unique=True, verbose_name='Титульник объявления')
    content = models.TextField(null=False, verbose_name='Содержание')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False, verbose_name='Цена')
    item_count = models.PositiveSmallIntegerField(default=0, null=False, verbose_name='Количество товара')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации')
    number_of_views = models.PositiveIntegerField(default=0, null=False, verbose_name='Количество просмотров')

    #Обновление количества оставшихся товаров после заказа
    def item_count_update(self, order_item_count):
        self.item_count -= order_item_count
        if self.item_count > 0:
            self.save()
        else:
            return f'Не хватает {self.item_count * -1}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        pass