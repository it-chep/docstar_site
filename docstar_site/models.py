from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Doctor(models.Model):
    """User Docstar"""
    name = models.CharField('ФИО', max_length=100)
    slug = models.SlugField("URL", max_length=225, unique=True, db_index=True)
    email = models.CharField('email', max_length=100, null=True)
    inst_url = models.CharField('Аккаунт инстаграм', max_length=100)
    vk_url = models.CharField('Аккаунт VK', max_length=100)
    dzen_url = models.CharField('Аккаунт Яндекс.Дзен', max_length=100)
    tg_url = models.CharField('Аккаунт TG', max_length=100)
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True)
    medical_directions = models.CharField('Направление медицины', max_length=100)
    speciallity = models.ForeignKey('Speciallity', on_delete=models.PROTECT, null=True)
    additional_speciallity = models.CharField('Доп специальность', max_length=100)
    main_blog_theme = models.CharField('Тематика блога', max_length=100)
    status_club = models.BooleanField('Подписка на клуб', null=True)
    avatar = models.ImageField("Личное фото", upload_to="user_photos/", null=True, default='user_photos/zag.png')
    doctor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    prodoctorov = models.CharField("ПРОДОКТОРОВ", null=True, max_length=255, unique=True)
    subscribers_inst = models.CharField("Подписчики инста", null=True,  max_length=255,)

    def __str__(self):
        return self.name

    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url

    def get_absolute_url(self):
        return reverse('doctor_card', kwargs={'slug': self.slug})

    def get_absolute_edit(self):
        return reverse('edit', kwargs={'slug': self.slug})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["name"]


class Lection(models.Model):
    """Docstar Lection"""
    lection_name = models.CharField('Название лекции', max_length=100)
    slug = models.SlugField("URL", max_length=225, unique=True, db_index=True)
    youtube_url = models.CharField('Cсылка на лекцию', max_length=100)
    pre_photo = models.ImageField('Превью к лекции', upload_to="photos/", null=True)
    lector_inst = models.CharField('Ссылка на инст лектора', max_length=100, null=True)

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
    name = models.CharField("Название города", max_length=100, db_index=True)
    code = models.CharField("Код города", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ["name"]


class Knowledge(models.Model):
    """Knowlrdge base"""

    name = models.CharField("Насзвание поста", max_length=100)
    tg_link = models.CharField("Ссылка на тг", max_length=100)
    slug = models.SlugField("URL", max_length=225, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'База знаний'
        verbose_name_plural = 'База знаний'
        ordering = ["name"]


class GetCourseExportID(models.Model):

    export_id = models.CharField("Export_id", max_length=40, unique=True)
    export_time = models.DateTimeField("Время экспорта", auto_now=True)

    def __str__(self):
        return self.export_id

    class Meta:
        verbose_name = 'Айдишник'
        verbose_name_plural = 'Айдишники'

