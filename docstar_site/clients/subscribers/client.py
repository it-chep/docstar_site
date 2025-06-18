from __future__ import annotations

from typing import Optional

import requests
from django.conf import settings

from docstar_site.clients.subscribers.dto import FilterDoctorsRequest, GetDoctorSubscribersResponse


class SubscribersClient:

    def __init__(self, url):
        self.url = url
        self.limit = settings.LIMIT_DOCTORS_ON_PAGE

    def filter_doctors_ids(self, request: FilterDoctorsRequest, *args, **kwargs) -> list[int]:
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

            if not all(key in data for key in ['doctors_ids']):
                raise ValueError("Неверные данные в ответе API")

            return data['doctors_ids']
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
                subs_count=data['telegram_short'],
                subs_count_text=data['telegram_text'],
                last_updated_date=data['tg_last_updated_date'],
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
            print("создание врача в subscribers", response.status_code, response.__dict__)
            if response.status_code == 400:
                return False

            # Проверка статус кода
            response.raise_for_status()
            return True

        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, ValueError, Exception) as e:
            return None

    def update_doctor(self, doctor_id: int, telegram: str, instagram: Optional[str], *args, **kwargs) -> bool:
        ...

    def filter_info(self):
        ...