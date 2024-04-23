from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer')

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'


class Contractor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='contractor')
    exprience = models.PositiveSmallIntegerField(verbose_name='Опыт работы')

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, title={self.title})'

    def get_absolute_url(self):
        return f'/orders/{self.id}/'


class Response(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='responses')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='responses')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
