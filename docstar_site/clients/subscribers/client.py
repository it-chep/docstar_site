from __future__ import annotations
from urllib.parse import quote
from typing import Optional

import requests
from django.conf import settings

from docstar_site.clients.subscribers.dto import FilterDoctorsRequest, GetDoctorSubscribersResponse, \
    DoctorMiniatureInfoResponse


class SubscribersClient:

    def __init__(self, url):
        self.url = url
        self.limit = settings.LIMIT_DOCTORS_ON_PAGE

    def filter_doctors_ids(self, request: FilterDoctorsRequest, *args, **kwargs) -> list[DoctorMiniatureInfoResponse]:
        # пока хардкодим ТГ, тк только с тг есть интеграшка
        api_url = f'{self.url}/doctors/filter?social_media=tg&max_subscribers={request.max_subscribers}&min_subscribers={request.min_subscribers}&offset={request.offset}'

        try:
            response = requests.get(
                api_url,
                timeout=3,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()

            data = response.json()

            if not all(key in data for key in ['doctors']):
                raise ValueError("Неверные данные в ответе API")

            doctors = []
            for doctor in data['doctors']:
                doctors.append(DoctorMiniatureInfoResponse(
                    doctor_id=doctor["doctor"]['doctor_id'],
                    tg_subs_count=doctor["doctor"]['telegram_short'],
                    tg_subs_count_text=doctor["doctor"]['telegram_text'],
                ))

            return doctors
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, ValueError, Exception) as e:
            return []

    def get_doctor_subscribers(self, doctor_id: int, *args, **kwargs) -> GetDoctorSubscribersResponse:
        api_url = f'{self.url}/subscribers/{doctor_id}/'

        try:
            response = requests.get(
                api_url,
                timeout=3,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()

            data = response.json()

            if not all(key in data for key in ['doctor_id', 'telegram']):
                raise ValueError("Неполные данные в ответе API")

            return GetDoctorSubscribersResponse(
                tg_subs_count=data['telegram_short'],
                tg_subs_count_text=data['telegram_text'],
                tg_last_updated_date=data['tg_last_updated_date'],
            )

        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, ValueError, Exception) as e:
            return GetDoctorSubscribersResponse(0, "", "")

    def create_doctor(self, doctor_id: int, telegram: str, instagram: Optional[str], *args, **kwargs) -> bool | None:
        """
        Создает нового доктора через API
        """
        api_url = f'{self.url}/doctors/create/'

        if not doctor_id or not telegram:
            return None

        # Подготовка данных для запроса
        body = {
            'doctor_id': doctor_id,
            'instagram': instagram,
            'telegram': telegram
        }

        # Удаляем None значения из payload
        payload = {k: v for k, v in body.items() if v is not None}

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        try:
            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            if response.status_code == 400:
                return False

            # Проверка статус кода
            response.raise_for_status()
            return True

        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, ValueError, Exception) as e:
            return None

    def update_doctor(self, doctor_id: int, telegram: str, instagram: Optional[str], *args, **kwargs) -> int:
        """
        Обновляет информацию о докторе
        """
        api_url = f'{self.url}/doctors/{doctor_id}/'

        if not doctor_id or not telegram:
            return None

        # Подготовка данных для запроса
        body = {
            'instagram': instagram,
            'telegram': telegram
        }

        # Удаляем None значения из payload
        payload = {k: v for k, v in body.items() if v is not None}

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        try:
            response = requests.patch(
                api_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            if response.status_code == 400:
                return response.status_code

            # Проверка статус кода
            response.raise_for_status()
            return response.status_code

        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, ValueError, Exception) as e:
            return 500

    def get_subscribers_by_doctors_ids(self, doctor_ids: list[int]) -> dict:
        """
        Получает количество подписчиков для миниатюр по переданным IDs
        """
        str_ids = [str(i).strip() for i in doctor_ids if str(i).strip()]
        encoded_ids = quote(",".join(str_ids))
        api_url = f'{self.url}/doctors/by_ids/?doctor_ids={encoded_ids}'
        try:
            response = requests.get(
                api_url,
                timeout=3,
                headers={'Content-Type': 'application/json'}
            )

            response.raise_for_status()
            response_data = response.json()

            dict_response = dict()
            for doctor_id, doctor_data in response_data['data'].items():
                dict_response[int(doctor_id)] = DoctorMiniatureInfoResponse(
                    doctor_id=int(doctor_data['doctor_id']),
                    tg_subs_count=doctor_data['telegram_subs_count'],
                    tg_subs_count_text=str(doctor_data['telegram_subs_text']),
                )
            return dict_response

        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, ValueError, Exception) as e:
            return dict()

    def filter_info(self):
        ...
