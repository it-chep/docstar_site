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
