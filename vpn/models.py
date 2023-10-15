import datetime

from django.db import models
from django.utils import timezone


class Blogger(models.Model):
    name = models.CharField(verbose_name='Имя Блогера', max_length=255, blank=False)
    username = models.CharField(verbose_name='Username Telegram блогера', max_length=255, blank=False)
    tg_id = models.BigIntegerField(verbose_name="Telegram_id", blank=False, unique=True)
    sb_id = models.BigIntegerField(verbose_name="Salebot_id", blank=False, unique=True)
    discount = models.IntegerField(verbose_name='Процент скидки', blank=True, default=10)
    utm = models.ForeignKey('UTM', on_delete=models.CASCADE, verbose_name='UTM-метка', null=True, blank=True)
    registration_date_time = models.DateTimeField(verbose_name="Дата регистрации", default=timezone.now)
    pay_date = models.IntegerField(verbose_name='Дата расчетов', blank=True, default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блогер'
        verbose_name_plural = 'Блогеры'


class UTM(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'UTM-метка'
        verbose_name_plural = 'UTM-метки'


class Client(models.Model):
    name = models.CharField(verbose_name='Имя клиента', max_length=255, blank=True)
    username = models.CharField(verbose_name='Username Telegram клиента', max_length=255, blank=True)
    tg_id = models.BigIntegerField(verbose_name="Telegram_id", blank=False, unique=True)
    sb_id = models.BigIntegerField(verbose_name="Salebot_id", blank=False, unique=True)
    gk_id = models.BigIntegerField(verbose_name="GetCourse_id", blank=False, unique=True)
    registration_date_time = models.DateTimeField(verbose_name="Дата регистрации", default=timezone.now)
    utm = models.ForeignKey('UTM', on_delete=models.CASCADE, verbose_name='UTM-метка', null=True, blank=True)
    blogger = models.ForeignKey('Blogger', on_delete=models.CASCADE, verbose_name='Блогер', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент купивший VPN'
        verbose_name_plural = 'Клиенты купившие VPN'
