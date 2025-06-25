from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class FilterDoctorsRequest:
    # соц.сеть
    social_media: str = "tg"
    # офсет
    offset: int = 0
    # лимит
    limit: int = 10
    # максимальное количество подписчиков
    max_subscribers: int = 0
    # минимальное количество подписчиков
    min_subscribers: int = 0


@dataclass
class GetDoctorSubscribersResponse:
    # количество подписчиков
    subs_count: int = 0
    # текст "подписчика", "подписчиков", "подписчик"
    subs_count_text: str = ""
    # дата последнего обновления в сервисе
    last_updated_date: str = ""


@dataclass
class DoctorMiniatureInfoResponse:
    # ID доктора
    doctor_id: int
    # количество подписчиков
    subs_count: int = 0
    # текст "подписчика", "подписчиков", "подписчик"
    subs_count_text: str = ""
