# Generated by Django 4.1.5 on 2025-01-07 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Мероприятие', 'verbose_name_plural': 'Мероприятия'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Билет на мероприятие', 'verbose_name_plural': 'Билеты на мероприятие'},
        ),
    ]
