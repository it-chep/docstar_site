# Generated by Django 4.1.5 on 2025-06-01 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docstar_site', '0008_doctor_s3_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='avatar',
            field=models.ImageField(blank=True, default='user_photos/zag.png', null=True, upload_to='user_photos/', verbose_name='Личное фото'),
        ),
    ]
