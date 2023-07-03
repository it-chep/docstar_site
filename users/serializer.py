import datetime
import random
import string
from django.core.mail import send_mail
from django.db.utils import ProgrammingError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import CustomUser


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'not_unique'})

        return data

    def create(self, validated_data):
        email = validated_data['email']
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

        user = CustomUser.objects.create(
            password=make_password(validated_data['password']),
            email=email,
            email_verification_token=random_string,
            verified_email=False,
            last_login=datetime.datetime.now()
        )

        send_mail(
            'Подтверждение email',
            'Привет, Вы только что зарегистрировались на сайте Тренажер Счастья. '
            'Но чтобы получить доступ к закрытым материалам, нам нужно проверить вашу почту. Чтобы пройти проверку,'
            f' нажмите на кнопку    '
            # f'<a href="http://127.0.0.1:8000/users/verificate_email/get_token/?token={random_string}" '
            f'<a href="https://docstar.readyschool.ru/users/verificate_email/get_token/?token={random_string}" '
            'style="display: inline-block; background-color: #01abaa; color: #fff; padding: 10px; " \
                  "text-decoration: none; border-radius: 5px;">Подтвердить почту</a>',
            'readymama@ya.ru',
            [f'{email}'],
            fail_silently=False,
            html_message='Привет, Вы только что зарегистрировались на сайте Тренажер Счастья. '
                         'Но чтобы получить доступ к закрытым материалам, нам нужно '
                         'проверить вашу почту. Чтобы пройти проверку,'
                         f' нажмите на кнопку    '
                         # f'<a href="http://127.0.0.1:8000/users/verificate_email/get_token/'
                         # f'?token={random_string}" '
                         f'<a href="https://docstar.readyschool.ru/users/verificate_email/get_token/'
                         f'?token={random_string}" '
                         'style="display: inline-block; background-color: #01abaa; color: #fff; padding: 10px; " \
                               "text-decoration: none; border-radius: 5px;">Подтвердить почту</a>',
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError({'user': 'invalid_data'})
        else:
            raise serializers.ValidationError({'user': 'incomplete'})
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

            user = CustomUser.objects.filter(email=email).get()
            pk = user.pk
            user.email_verification_token = random_string
            user.save()

            # asya = AsyncUsers()
            # token_delay.delay(pk)

            send_mail(
                'Восстановление пароля',
                'Привет, вижу, что вы забыли пароль 🙁'
                'Чтобы восстановить доступ к аккунту нажмите на кнопку '
                f'<a href="https://docstar.readyschool.ru/users/forgot_passw'
                f'ord/validate_token/?token={random_string}" '
                'style="display: inline-block; background-color: #01abaa; color: #fff; padding: 10px; " \
                  "text-decoration: none; border-radius: 5px;">Восстановить пароль</a>',
                'readymama@ya.ru',
                [email],
                fail_silently=False,
                html_message='Привет, вижу, что вы забыли пароль 🙁'
                             'Чтобы восстановить доступ к аккунту нажмите на кнопку '
                             f'<a href='
                             f'"https://docstar.readyschool.ru/users/forgot_password/validate_'
                             f'token/?token={random_string}" '
                             'style="display: inline-block; background-color: #01abaa; color: #fff; padding: 10px; " \
                               "text-decoration: none; border-radius: 5px;">Восстановить пароль</a>',
            )

        else:
            raise serializers.ValidationError({'email': 'not_exist'})

        return data


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        # Поменять пароль и вернуть пользователя, чтобы залогинить его
        # print(password)
        if CustomUser.objects.filter(email_verification_token=data['token']).exists():
            user = CustomUser.objects.filter(email_verification_token=data['token']).get()
            user.set_password(data['password'])
            # user.password = data['password']
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error': 'invalid_serializer'})
