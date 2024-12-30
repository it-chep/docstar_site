from django.db import models


class Event(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название мероприятия",
        null=True,
        blank=True
    )
    capacity = models.IntegerField(
        verbose_name="Количество мест на мероприятии",
        null=True,
        blank=True
    )
    event_date = models.DateField(
        verbose_name="Дата проведения мероприятия",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"


class Ticket(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name="Мероприятие",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    email = models.CharField(
        max_length=255,
        verbose_name="Email",
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания тикета"
    )

    class Meta:
        verbose_name = "Билет на мероприятие"
        verbose_name_plural = "Билеты на мероприятие"
