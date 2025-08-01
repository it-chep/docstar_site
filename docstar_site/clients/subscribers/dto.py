from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class FilterDoctorsRequest:
    # соц.сеть
    social_media: list[str] = list["tg"]
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
    tg_subs_count: int = 0
    # текст "подписчика", "подписчиков", "подписчик"
    tg_subs_count_text: str = ""
    # дата последнего обновления в сервисе
    tg_last_updated_date: str = ""
    # количество подписчиков
    inst_subs_count: int = 0
    # текст "подписчика", "подписчиков", "подписчик"
    inst_subs_count_text: str = ""
    # дата последнего обновления в сервисе
    inst_last_updated_date: str = ""


@dataclass
class DoctorMiniatureInfoResponse:
    # ID доктора
    doctor_id: int
    # количество подписчиков
    tg_subs_count: str = "0"
    # текст "подписчика", "подписчиков", "подписчик"
    tg_subs_count_text: str = ""
    # количество подписчиков
    inst_subs_count: str = "0"
    # текст "подписчика", "подписчиков", "подписчик"
    inst_subs_count_text: str = ""


@dataclass
class FilterInfoResponse:
    # Название для пользователя
    name: str
    # Для фильтрации в базе
    slug: str

@dataclass
class GetAllSubscribersInfoResponse:
    # количество подписчиков
    subscribers_count: str = ""
    # текст "подписчика", "подписчиков", "подписчик"
    subscribers_count_text: str = ""
    # дата последнего обновления в сервисе
    last_updated: str = ""