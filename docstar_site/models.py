from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Doctor(models.Model):
    """User Docstar"""
    name = models.CharField(verbose_name='ФИО', max_length=100)
    slug = models.SlugField(verbose_name="URL", max_length=225, unique=True, db_index=True)
    email = models.CharField(verbose_name='email', max_length=100, null=True)

    inst_url = models.CharField(verbose_name='Аккаунт инстаграм', max_length=100, null=True, blank=True)
    vk_url = models.CharField(verbose_name='Аккаунт VK', max_length=100, null=True, blank=True)
    dzen_url = models.CharField(verbose_name='Аккаунт Яндекс.Дзен', max_length=100, null=True, blank=True)
    tg_url = models.CharField(verbose_name='Аккаунт TG', max_length=100, null=True, blank=True)
    youtube_url = models.CharField(verbose_name='Аккаунт YOUTUBE', max_length=100, null=True, blank=True)

    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Город")
    medical_directions = models.CharField(verbose_name='Направление медицины', max_length=255, null=True, blank=True)
    speciallity = models.ForeignKey('Speciallity', on_delete=models.PROTECT, null=True, verbose_name="Специальность")
    additional_speciallity = models.CharField('Доп специальность', max_length=255, null=True, blank=True)
    main_blog_theme = models.TextField(verbose_name='Тематика блога', null=True, blank=True)

    status_club = models.BooleanField(verbose_name='Подписка на клуб', null=True)
    avatar = models.ImageField(
        verbose_name="Личное фото",
        upload_to="user_photos/",
        null=True,
        default='user_photos/zag.png'
    )
    doctor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    prodoctorov = models.CharField(verbose_name="ПРОДОКТОРОВ", null=True, max_length=255, unique=True, blank=True)
    subscribers_inst = models.CharField(verbose_name="Подписчики инста", null=True, max_length=255, blank=True)

    is_active = models.BooleanField(verbose_name='Показывать доктора', default=True)

    def __str__(self):
        return self.name

    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url

    def get_absolute_url(self):
        return reverse('doctor_card', kwargs={'slug': self.slug})

    def get_absolute_edit(self):
        return reverse('edit', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ["name"]


class Lection(models.Model):
    """Docstar Lection"""
    lection_name = models.CharField(verbose_name='Название лекции', max_length=100)
    slug = models.SlugField(verbose_name="URL", max_length=225, unique=True, db_index=True)
    youtube_url = models.CharField(verbose_name='Cсылка на лекцию', max_length=100)
    pre_photo = models.ImageField(verbose_name='Превью к лекции', upload_to="photos/", null=True)
    lector_inst = models.CharField(verbose_name='Ссылка на инст лектора', max_length=100, null=True)

    def __str__(self):
        return self.lection_name

    def yt_link(self):
        if self.youtube_url and hasattr(self.youtube_url, 'url'):
            return self.youtube_url.url

    def get_absolute_url(self):
        return reverse('lection_card', kwargs={'lection_id': self.pk})

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'
        ordering = ["lection_name"]


class Speciallity(models.Model):
    """Users Speciallity"""
    name = models.CharField("Название специальности", max_length=100, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ["name"]


class City(models.Model):
    """Users City"""
    name = models.CharField(verbose_name="Название города", max_length=100, db_index=True)
    code = models.CharField(verbose_name="Код города", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ["name"]


class Knowledge(models.Model):
    """Knowlrdge base"""

    name = models.CharField(verbose_name="Насзвание поста", max_length=100)
    tg_link = models.CharField(verbose_name="Ссылка на тг", max_length=100)
    slug = models.SlugField(verbose_name="URL", max_length=225, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'База знаний'
        verbose_name_plural = 'База знаний'
        ordering = ["name"]


class GetCourseExportID(models.Model):
    export_id = models.CharField(verbose_name="Export_id", max_length=40, unique=True)
    export_time = models.DateTimeField(verbose_name="Время экспорта", auto_now=True)

    def __str__(self):
        return self.export_id

    class Meta:
        verbose_name = 'Айдишник'
        verbose_name_plural = 'Айдишники'
