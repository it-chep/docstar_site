from typing import Optional

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from docstar_site.clients.s3.client import DEFAULT_DOCTOR_IMAGE

User = settings.AUTH_USER_MODEL


class CooperationType(models.IntegerChoices):
    """Типы размещения врачей"""
    UNKNOWN = 0, "Неизвестно"
    CLUB_6_PLUS = 1, "Клуб 6+ месяцев"
    ADVERTISING_BARTER = 2, "Бартер по рекламе"
    PAID_FOREVER = 3, "Платно навсегда"
    SUBSCRIPTION = 4, "Подписка"
    READYDOC_PARDON = 5, "Помилование от READYDOC"


class Doctor(models.Model):
    """User Docstar"""
    name = models.CharField(verbose_name='ФИО', max_length=100)
    slug = models.SlugField(verbose_name="URL", max_length=225, unique=True, db_index=True)
    email = models.CharField(verbose_name='email', max_length=100, null=True)

    inst_url = models.CharField(verbose_name='Аккаунт инстаграм', max_length=100, null=True, blank=True)
    vk_url = models.CharField(verbose_name='Аккаунт VK', max_length=100, null=True, blank=True)
    dzen_url = models.CharField(verbose_name='Аккаунт Яндекс.Дзен', max_length=100, null=True, blank=True)
    tg_url = models.CharField(verbose_name='Аккаунт TG', max_length=100, null=True, blank=True)
    tg_channel_url = models.CharField(verbose_name='Канал TG', max_length=100, null=True, blank=True)
    youtube_url = models.CharField(verbose_name='Аккаунт YOUTUBE', max_length=100, null=True, blank=True)
    tiktok_url = models.CharField(verbose_name='Аккаунт TikTok', max_length=100, null=True, blank=True)

    medical_directions = models.CharField(verbose_name='Направление медицины', max_length=255, null=True, blank=True)

    city = models.ForeignKey(
        'City',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Город",
        related_name='doctors_primary',
    )

    additional_cities = models.ManyToManyField(
        'City',
        blank=True,
        verbose_name="Дополнительные города",
        related_name='doctors_additional'
    )  # + содержит основной город

    speciallity = models.ForeignKey(
        'Speciallity',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Специальность",
        related_name='doctors_primary',
    )

    additional_specialties = models.ManyToManyField(
        'Speciallity',
        blank=True,
        verbose_name="Дополнительные специальности",
        related_name='doctors_additional'
    )  # + содержит основную специальность

    additional_speciallity = models.CharField('Доп специальность', max_length=255, null=True, blank=True)
    main_blog_theme = models.TextField(verbose_name='Тематика блога', null=True, blank=True, max_length=500)

    avatar = models.ImageField(
        verbose_name="Личное фото",
        upload_to="user_photos/",
        null=True,
        blank=True,
        default='user_photos/zag.png'
    )
    doctor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    prodoctorov = models.CharField(verbose_name="Ссылка для записи", null=True, max_length=255, unique=False,
                                   blank=True)
    subscribers_inst = models.CharField(verbose_name="Подписчики инста", null=True, max_length=255, blank=True)

    age = models.IntegerField(verbose_name="Возраст", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    is_active = models.BooleanField(verbose_name='Показывать доктора', default=True)
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, null=True, blank=True)

    s3_image = models.CharField(max_length=255, null=True, blank=True)

    cooperation_type = models.SmallIntegerField(
        verbose_name="Тип размещения",
        choices=CooperationType.choices,
        default=CooperationType.UNKNOWN,
        null=True,
        blank=True
    )

    marketing_preferences = models.CharField(
        verbose_name="У врачей каких специальностей вы бы хотели приобрести рекламу / договориться о коллаборации?",
        max_length=300,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('doctor_card', kwargs={'slug': self.slug})

    def get_absolute_edit(self):
        return reverse('edit', kwargs={'slug': self.slug})

    def get_cooperation_display(self) -> str:
        """Возвращает читаемое название типа сотрудничества"""
        return self.get_cooperation_type_display()

    @property
    def avatar_url(self) -> str:
        """Динамически генерирует URL при запросе"""
        # возвращает либо файл с s3, либо с диска, либо дефолтный
        s3_file = self.get_s3_file
        if s3_file:
            return s3_file

        local_file = self.get_local_file
        if local_file:
            return local_file

        return DEFAULT_DOCTOR_IMAGE

    @property
    def get_local_file(self) -> Optional[str]:
        if self.avatar and hasattr(self.avatar, 'url'):
            try:
                # Если файл не удален, то возвращаем его
                _ = self.avatar.file
                return self.avatar.url
            except Exception:
                return None
        return None

    @property
    def get_s3_file(self) -> Optional[str]:
        if self.s3_image:
            url = settings.S3_CLIENT.generate_presigned_url(self.s3_image)
            if url:
                return url
        return None

    def save(self, *args, **kwargs):
        """Сохраняет файл в S3 и записывает ключ"""
        if settings.DEBUG:
            super().save(*args, **kwargs)
            return

        file_obj = self.avatar
        if file_obj:
            self.s3_image = f"images/user_{self.slug}_{file_obj.file.name}"
            if file_obj and not settings.S3_CLIENT.put_object(file_obj.file, self.s3_image):
                raise Exception("Не удалось сохранить фотку")
            self.avatar = None

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Удаляет файл из S3 при удалении модели"""
        settings.S3_CLIENT.delete_file(self.s3_image)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ["name"]


class Speciallity(models.Model):
    """Users Speciallity"""
    name = models.CharField("Название специальности", max_length=100, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специальность врача'
        verbose_name_plural = 'Специальности врачей'
        ordering = ["name"]


class City(models.Model):
    """Users City"""
    name = models.CharField(verbose_name="Название города", max_length=100, db_index=True)
    code = models.CharField(verbose_name="Код города", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город врача'
        verbose_name_plural = 'Города врачей'
        ordering = ["name"]


class GetCourseExportID(models.Model):
    export_id = models.CharField(verbose_name="Export_id", max_length=40, unique=True)
    export_time = models.DateTimeField(verbose_name="Время экспорта", auto_now=True)

    def __str__(self):
        return self.export_id

    class Meta:
        verbose_name = 'Айдишник'
        verbose_name_plural = 'Айдишники'


# ------------- Фрилансеры -----------------------

class FreelancersSpeciality(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название специальности")

    class Meta:
        verbose_name = "Специальность фрилансера"
        verbose_name_plural = "Специальности фрилансеров"
        db_table = "freelancers_speciality"

    def __str__(self):
        return self.name


class FreelancersCity(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название города")

    class Meta:
        verbose_name = "Город фрилансера"
        verbose_name_plural = "Города фрилансеров"
        db_table = "freelancers_city"

    def __str__(self):
        return self.name


class SocialNetworks(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название соцсети")
    slug = models.CharField(max_length=30, verbose_name="Слаг")

    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"
        db_table = "social_networks"

    def __str__(self):
        return self.name


class FreelancerCooperationType(models.Model):
    name = models.TextField(verbose_name="Название типа размещения")

    class Meta:
        verbose_name = "Тип размещения фрилансеров"
        verbose_name_plural = "Фрилансеры Типы размещения"
        db_table = "freelancers_cooperation_type"

    def __str__(self):
        return self.name


class Freelancer(models.Model):
    email = models.CharField(max_length=255, verbose_name="Email фрилансера")
    slug = models.TextField(verbose_name="Slug", null=False, blank=False)
    name = models.CharField(max_length=255, verbose_name="Имя", null=False, blank=False)
    is_worked_with_doctors = models.BooleanField(verbose_name="Опыт работы с врачами", default=False)
    is_active = models.BooleanField(verbose_name="Активен", default=False)
    tg_username = models.CharField(max_length=255, verbose_name="Telegram username", null=True, blank=True)
    portfolio_link = models.CharField(max_length=255, verbose_name="Ссылка на портфолио", null=True, blank=True)
    speciality = models.ForeignKey(
        FreelancersSpeciality,
        on_delete=models.SET_NULL,
        verbose_name="Основная специальность",
        null=True,
        blank=True,
        related_name='primary_freelancers'
    )
    city = models.ForeignKey(
        FreelancersCity,
        on_delete=models.SET_NULL,
        verbose_name="Основной город",
        null=True,
        blank=True,
        related_name='primary_freelancers'
    )
    price_category = models.IntegerField(verbose_name="Ценовая категория", null=True, blank=True)
    s3_image = models.TextField(verbose_name="Фотография", null=True, blank=True)

    avatar = models.ImageField(
        verbose_name="Личное фото",
        upload_to="user_photos/",
        null=True,
        blank=True,
        default='user_photos/zag.png'
    )

    cooperation_type = models.ForeignKey(
        FreelancerCooperationType,
        on_delete=models.SET_NULL,
        verbose_name="Тип размещения",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Фрилансер"
        verbose_name_plural = "Фрилансеры"
        unique_together = ('email', 'name')
        db_table = "freelancer"

    def __str__(self):
        return self.name

    @property
    def get_s3_file(self) -> Optional[str]:
        if self.s3_image:
            url = settings.S3_FREELANSERS_CLIENT.generate_presigned_url(self.s3_image)
            if url:
                return url
        return None

    def save(self, *args, **kwargs):
        """Сохраняет файл в S3 и записывает ключ"""
        # if settings.DEBUG:
        #     super().save(*args, **kwargs)
        #     return

        file_obj = self.avatar
        if file_obj:
            self.s3_image = f"images/user_{self.slug}_{file_obj.file.name}"
            if file_obj and not settings.S3_FREELANSERS_CLIENT.put_object(file_obj.file, self.s3_image):
                raise Exception("Не удалось сохранить фотку")
            self.avatar = None

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Удаляет файл из S3 при удалении модели"""
        settings.S3_FREELANSERS_CLIENT.delete_file(self.s3_image)
        super().delete(*args, **kwargs)


class FreelancerSpecialityM2M(models.Model):
    speciality = models.ForeignKey(FreelancersSpeciality, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Специальность фрилансера (M2M)"
        verbose_name_plural = "Специальности фрилансеров (M2M)"
        unique_together = ('speciality', 'freelancer')
        db_table = "freelancer_speciality_m2m"

    def __str__(self):
        return self.freelancer.name + self.speciality.name


class FreelancerCityM2M(models.Model):
    city = models.ForeignKey(FreelancersCity, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Город фрилансера (M2M)"
        verbose_name_plural = "Города фрилансеров (M2M)"
        unique_together = ('city', 'freelancer')
        db_table = "freelancer_city_m2m"

    def __str__(self):
        return self.freelancer.name + self.city.name


class FreelancerSocialNetworksM2M(models.Model):
    social_network = models.ForeignKey(SocialNetworks, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Соцсеть фрилансера (M2M)"
        verbose_name_plural = "Соцсети фрилансеров (M2M)"
        unique_together = ('social_network', 'freelancer')
        db_table = "freelancer_social_networks_m2m"

    def __str__(self):
        return self.freelancer.name + self.social_network.name


class FreelancersPriceList(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, verbose_name="Фрилансер")
    name = models.CharField(max_length=255, verbose_name="Название услуги")
    price = models.IntegerField(verbose_name="Стоимость услуги")

    class Meta:
        verbose_name = "Прайс-лист фрилансера"
        verbose_name_plural = "Прайс-листы фрилансеров"
        unique_together = ('freelancer', 'name')
        db_table = "freelancers_price_list"

    def __str__(self):
        return self.freelancer.name + self.name
