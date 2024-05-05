from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify as django_slugify
from langdetect import detect
from transliterate import slugify


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')


class Customer(CustomUser):

    is_customer = models.BooleanField(default=True, verbose_name='Заказчик')

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.username

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'


class Contractor(CustomUser):
    exprience = models.PositiveSmallIntegerField(verbose_name='Опыт работы')
    is_contractor = models.BooleanField(default=True, verbose_name='Исполнитель')

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return self.username

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'


class IsOrderActive(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='Заказчик')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL', blank=True, null=True)

    objects = models.Manager()
    active = IsOrderActive()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        unique_together = ('customer', 'title')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, title={self.title})'

    def get_absolute_url(self):
        return f'/orders/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug:
            title_lang = detect(self.title)
            username_lang = detect(self.customer.username)
            if title_lang == 'ru':
                if username_lang == 'ru':
                    self.slug = f'{slugify(self.customer.username)}-{slugify(self.title)}'
                else:
                    self.slug = f'{django_slugify(self.customer.username)}-{slugify(self.title)}'
            else:
                if username_lang == 'ru':
                    self.slug = f'{slugify(self.customer.username)}-{django_slugify(self.title)}'
                else:
                    self.slug = f'{django_slugify(self.customer.username)}-{django_slugify(self.title)}'
        super().save(*args, **kwargs)


class Response(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='responses', verbose_name='Заказ')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE,
                                   related_name='responses', verbose_name='Исполнитель')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        if len(self.message) <= 30:
            return self.message
        return f'{self.message[0:30]}...'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def get_absolute_url(self):
        return f'/responses/{self.id}/'
