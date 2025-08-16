import datetime
import re

from atatus.contrib.django.client import client
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from docstar_site.functions import get_eng_slug
from docstar_site.models import Speciallity, Doctor, City


class UpdateDoc(forms.ModelForm):
    avatar = forms.ImageField(label='Ваше фото', localize=False)

    class Meta:
        model = Doctor
        fields = ("avatar",)


class DoctorSearchForm(forms.Form):
    specialty = forms.ModelChoiceField(queryset=Speciallity.objects.all(), required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(DoctorSearchForm, self).__init__(*args, **kwargs)


class CreateDoctorForm(forms.Form):
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(attrs={'class': 'input-field'}),
        required=True,
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'}),
        required=True,
    )
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'}),
        required=True,
    )
    middle_name = forms.CharField(
        label='Отчество',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'}),
        required=True,
    )
    birth_date = forms.DateField(
        label='Ваш день рождения',
        widget=forms.TextInput(attrs={
            'class': 'datepicker',
            'placeholder': 'Укажите дату в формате ДД.ММ.ГГГГ',
        }),
        required=True,
    )

    additional_cities = forms.CharField(
        label='Дополнительные города',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'select-multiple',
            'placeholder': 'Выберите города'
        })
    )

    additional_specialties = forms.CharField(
        label='Дополнительные специальности',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'select-multiple',
            'placeholder': 'Выберите специальность'
        })
    )

    instagram_username = forms.CharField(
        label='Ваш никнейм в инстаграм',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Можете оставить пустым'
        }),
    )
    vk_username = forms.CharField(
        label='Ссылка на VK',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Можете оставить пустым'
        }),
    )
    telegram_username = forms.CharField(
        label='Ваш никнейм в Telegram (не канал, а личный никнейм, через @)',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Пример: @readydoc'
        }),
    )
    dzen_username = forms.CharField(
        label='Ссылка на ЯндексДзен',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Можете оставить пустым'
        }),
    )
    youtube_username = forms.CharField(
        label='Ссылка на YouTube',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Можете оставить пустым'
        }),
    )

    telegram_channel = forms.CharField(
        label='Ссылка на ваш канал в телеграм',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Пример: https://t.me/readydoctor, но можно оставить пустым'
        }),
    )

    city = forms.ChoiceField(
        label='Выберите город (Если вашего нет, напишите об этом в бота)',
        required=True,
        # choices=[(None, None)] + [(city.id, city.name) for city in City.objects.all()]
    )
    speciallity = forms.ChoiceField(
        label='Выберите вашу специальность (Если ее нет, напишите в бота)',
        required=True,
        # choices=[(None, None)] + [(spec.id, spec.name) for spec in Speciallity.objects.all()]
    )
    main_blog_theme = forms.CharField(
        label='ТОП-5 заболеваний/тем про которые пишете в блоге',
        widget=forms.TextInput(attrs={
            'placeholder': ''
        }),
        required=True,
    )
    marketing_preferences = forms.CharField(
        label='У врачей каких специальностей вы бы хотели приобрести рекламу / договориться о коллаборации? (Планируем сделать вкладку «ищу неврологов, гинекологов и т.д.)',
        required=True,
    )
    prodoctorov = forms.CharField(
        label='Ваш сайт/таплинк',
        widget=forms.TextInput(attrs={
            'placeholder': 'Пример: https://taplink.cc/readydoc'
        }),
        required=False,
    )

    agree_policy = forms.BooleanField(
        label='Согласен с политикой обработки данных', required=True
    )

    def clean(self):
        if all([
            not self.cleaned_data.get('instagram_username'),
            not self.cleaned_data.get('vk_username'),
            not self.cleaned_data.get('telegram_username'),
            not self.cleaned_data.get('telegram_channel'),
            not self.cleaned_data.get('dzen_username'),
            not self.cleaned_data.get('youtube_username'),
        ]):
            error = 'Обязательно нужно указать хотя бы 1 вашу соцсеть'
            self.add_error('instagram_username', error)
            raise ValidationError(error)

        super().clean()
        if self.cleaned_data.get('last_name') and self.cleaned_data.get('first_name') and self.cleaned_data.get(
                'middle_name'):
            self.name = f"{self.cleaned_data.get('last_name').strip()} {self.cleaned_data.get('first_name').strip()} {self.cleaned_data.get('middle_name').strip()}"

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if "(" in last_name or ")" in last_name:
            raise ValidationError("Указаны недопустимые символы, можно указать только 1 фамилию")

    def clean_city(self):
        city_id = self.cleaned_data.get('city')
        if not city_id:
            raise ValidationError('Обязательное поле.')
        if City.objects.filter(id=int(city_id)).exists():
            return city_id
        raise ValidationError('Указанного города не существует.')

    def clean_speciallity(self):
        speciallity_id = self.cleaned_data.get('speciallity')
        if not speciallity_id:
            raise ValidationError('Обязательное поле.')
        if Speciallity.objects.filter(id=int(speciallity_id)).exists():
            return speciallity_id
        raise ValidationError('Указанной специальности не существует.')

    def _clean_social_link(self, field_value, platform_url):
        """Общая логика для обработки ссылок."""
        if not field_value:
            return field_value

        field_value = field_value.strip()

        if not field_value.startswith("https://"):
            if field_value.startswith("@"):
                field_value = field_value[1:]

            field_value = f"{platform_url}{field_value}"

        return field_value

    def clean_instagram_username(self):
        data = self.cleaned_data.get("instagram_username")
        inst_link = self._clean_social_link(data, "https://instagram.com/")
        if inst_link:
            return inst_link.lower()
        return inst_link

    def clean_vk_username(self):
        data = self.cleaned_data.get("vk_username")
        return self._clean_social_link(data, "https://vk.com/")

    def clean_dzen_username(self):
        data = self.cleaned_data.get("dzen_username")
        return self._clean_social_link(data, "https://dzen.ru/")

    def clean_youtube_username(self):
        data = self.cleaned_data.get("youtube_username")
        return self._clean_social_link(data, "https://youtube.com/")

    def clean_telegram_channel(self):
        data = self.cleaned_data.get("telegram_channel")
        return self._clean_social_link(data, "https://t.me/")

    def clean_prodoctorov(self):
        data = self.cleaned_data.get("prodoctorov")
        if not data:
            return ""
        if "t.me" in data or "@" in data or "vk.com" in data or "instagram.com" in data or "youtube.com" in data or "dzen.ru" in data:
            raise ValidationError("Пожалуйста, укажите ссылку на сайт, а не на соц.сеть")
        if data and "http" not in data and not data[0:4] == "http":
            raise ValidationError("Пожалуйста, укажите ссылку на сайт, ссылка должна содержать http")
        return self._clean_social_link(data, "")

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if not birth_date:
            raise ValidationError('Дата рождения обязательна.')

        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', birth_date.strftime('%d.%m.%Y')):
            raise ValidationError('Неверный формат даты. Ожидается ДД.ММ.ГГГГ.')

        if birth_date > datetime.date.today():
            raise ValidationError('Дата рождения не может быть в будущем.')

        max_age_date = datetime.date.today().replace(year=datetime.date.today().year - 120)
        if birth_date < max_age_date:
            raise ValidationError('Дата рождения не должна быть старше 120 лет.')

        return birth_date

    def save(self, commit=True):
        try:
            existing_doctor = Doctor.objects.filter(
                name=self.name,
                email=self.cleaned_data["email"]
            ).first()
            if existing_doctor:
                # Обновляем существующего врача
                existing_doctor.inst_url = self.cleaned_data["instagram_username"]
                existing_doctor.vk_url = self.cleaned_data["vk_username"]
                existing_doctor.dzen_url = self.cleaned_data["dzen_username"]
                existing_doctor.tg_url = self.cleaned_data["telegram_username"]
                existing_doctor.tg_channel_url = self.cleaned_data["telegram_channel"]
                existing_doctor.youtube_url = self.cleaned_data["youtube_username"]
                existing_doctor.city_id = self.cleaned_data["city"]
                existing_doctor.speciallity_id = self.cleaned_data["speciallity"]
                existing_doctor.main_blog_theme = self.cleaned_data["main_blog_theme"]
                existing_doctor.birth_date = self.cleaned_data["birth_date"]
                existing_doctor.prodoctorov = self.cleaned_data["prodoctorov"]
                existing_doctor.marketing_preferences = self.cleaned_data["marketing_preferences"]

                existing_doctor.save()

                # Обработка дополнительных городов
                ids_str = self.cleaned_data["additional_cities"].strip("[]'\"")
                ids_list = ids_str.split(',')
                city_ids = [int(city_id.strip()) for city_id in ids_list if city_id.strip().isdigit()]
                city_ids.append(self.cleaned_data["city"])
                existing_doctor.additional_cities.set(city_ids)

                ids_str = self.cleaned_data["additional_specialties"].strip("[]'\"")
                ids_list = ids_str.split(',')
                specialties_ids = [int(city_id.strip()) for city_id in ids_list if city_id.strip().isdigit()]
                specialties_ids.append(self.cleaned_data["speciallity"])
                existing_doctor.additional_specialties.set(specialties_ids)

                return existing_doctor
            else:
                slug = get_eng_slug(self.name)
                doctor = Doctor(
                    name=self.name,
                    slug=slug,
                    email=self.cleaned_data["email"],
                    inst_url=self.cleaned_data["instagram_username"],
                    vk_url=self.cleaned_data["vk_username"],
                    dzen_url=self.cleaned_data["dzen_username"],
                    tg_url=self.cleaned_data["telegram_username"],
                    tg_channel_url=self.cleaned_data["telegram_channel"],
                    youtube_url=self.cleaned_data["youtube_username"],
                    city_id=self.cleaned_data["city"],
                    speciallity_id=self.cleaned_data["speciallity"],
                    main_blog_theme=self.cleaned_data["main_blog_theme"],
                    birth_date=self.cleaned_data["birth_date"],
                    prodoctorov=self.cleaned_data["prodoctorov"],
                    marketing_preferences=self.cleaned_data["marketing_preferences"],
                    is_active=False,
                )

                doctor.save()

                # Обработка дополнительных городов
                ids_str = self.cleaned_data["additional_cities"].strip("[]'\"")
                ids_list = ids_str.split(',')
                city_ids = [int(city_id.strip()) for city_id in ids_list if city_id.strip().isdigit()]
                city_ids.append(self.cleaned_data["city"])
                doctor.additional_cities.set(city_ids)

                ids_str = self.cleaned_data["additional_specialties"].strip("[]'\"")
                ids_list = ids_str.split(',')
                specialties_ids = [int(city_id.strip()) for city_id in ids_list if city_id.strip().isdigit()]
                specialties_ids.append(self.cleaned_data["speciallity"])
                doctor.additional_specialties.set(specialties_ids)

                return doctor
        except City.DoesNotExist:
            raise ValidationError('Указанный город не найден.')
        except Speciallity.DoesNotExist:
            raise ValidationError('Указанная специальность не найдена.')
        except Exception as e:
            print(e)
            raise ValidationError(f'Произошла ошибка: {e}')
