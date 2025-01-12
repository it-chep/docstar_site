import datetime
import re

from django import forms
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
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'}),
    )
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'}),
    )
    middle_name = forms.CharField(
        label='Отчество',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'}),
    )

    age = forms.IntegerField(
        label='Сколько вам лет',
        min_value=0,
    )
    birth_date = forms.DateField(
        label='Ваш день рождения',
        widget=forms.TextInput(attrs={
            'class': 'datepicker',
            'placeholder': 'Укажите дату в формате ДД.ММ.ГГГГ',
        }),
    )

    instagram_username = forms.CharField(
        label='Ваш никнейм в инстаграм',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Можете оставить пустым'
        }),
    )
    instagram_subscribers = forms.IntegerField(
        label='Количество подписчиков в Инстаграм (целое число)',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
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
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Можете оставить пустым'
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

    city = forms.ChoiceField(
        label='Выберите город (Если вашего нет, напишите об этом в бота)',
        required=True,
        choices=[(None, None)] + [(city.id, city.name) for city in City.objects.all()]
    )
    speciallity = forms.ChoiceField(
        label='Выберите вашу специальность (Если ее нет, напишите в бота)',
        required=True,
        choices=[(None, None)] + [(spec.id, spec.name) for spec in Speciallity.objects.all()]
    )

    medical_directions = forms.CharField(
        label='Направление медицины',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Можете оставить пустым'
        }),
    )
    additional_speciallity = forms.CharField(
        label='Дополнительная специальность',
        widget=forms.TextInput(attrs={
            'placeholder': 'Если нет, можете не указывать'
        }),
        required=False,
    )
    main_blog_theme = forms.CharField(
        label='Основная тематика блога',
        required=False,
    )
    prodoctorov = forms.CharField(
        label='Куда записываться к вам на прием?',
        required=False,
    )

    # agree_policy = forms.BooleanField(
    #     label='Согласен с политикой обработки данных', required=True
    # )

    def clean(self):
        if all([
            not self.cleaned_data.get('instagram_username'),
            not self.cleaned_data.get('vk_username'),
            not self.cleaned_data.get('telegram_username'),
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

    def clean_city(self):
        city_id = self.cleaned_data.get('city')
        if not city_id:
            raise ValidationError('Обязательное поле.')
        if city := City.objects.filter(id=city_id).exists():
            return city
        raise ValidationError('Указанного города не существует.')

    def clean_speciallity(self):
        speciallity_id = self.cleaned_data.get('speciallity')
        if not speciallity_id:
            raise ValidationError('Обязательное поле.')
        if speciallity := Speciallity.objects.filter(id=speciallity_id).exists():
            return speciallity
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
        return self._clean_social_link(data, "https://instagram.com/")

    def clean_vk_username(self):
        data = self.cleaned_data.get("vk_username")
        return self._clean_social_link(data, "https://vk.com/")

    def clean_dzen_username(self):
        data = self.cleaned_data.get("dzen_username")
        return self._clean_social_link(data, "https://dzen.ru/")

    def clean_youtube_username(self):
        data = self.cleaned_data.get("youtube_username")
        return self._clean_social_link(data, "https://youtube.com/")

    def clean_prodoctorov(self):
        data = self.cleaned_data.get("prodoctorov")
        if not data:
            data = self.cleaned_data.get("instagram_username")
            return self._clean_social_link(data, "https://instagram.com/")
        return self._clean_social_link(data, "")

    def save(self, commit=True):
        try:
            slug = get_eng_slug(self.name)
            doctor = Doctor.objects.create(
                name=self.name,
                slug=slug,
                email=self.cleaned_data["email"],
                inst_url=self.cleaned_data["instagram_username"],
                vk_url=self.cleaned_data["vk_username"],
                dzen_url=self.cleaned_data["dzen_username"],
                tg_url=self.cleaned_data["telegram_username"],
                youtube_url=self.cleaned_data["youtube_username"],
                city_id=self.cleaned_data["city"],
                medical_directions=self.cleaned_data["medical_directions"],
                speciallity_id=self.cleaned_data["speciallity"],
                additional_speciallity=self.cleaned_data["additional_speciallity"],
                main_blog_theme=self.cleaned_data["main_blog_theme"],
                age=self.cleaned_data["age"],
                birth_date=self.cleaned_data["birth_date"],
                prodoctorov=self.cleaned_data["prodoctorov"],
                subscribers_inst=self.cleaned_data["instagram_subscribers"],
            )
            return doctor
        except City.DoesNotExist:
            raise ValidationError('Указанный город не найден.')
        except Speciallity.DoesNotExist:
            raise ValidationError('Указанная специальность не найдена.')
        except Exception as e:
            raise ValidationError(f'Произошла ошибка: {e}')
