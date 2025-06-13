from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FilterDoctorsRequest:
    # соц.сеть
    social_media: str
    # офсет
    offset: int
    # лимит
    limit: int
    # максимальное количество подписчиков
    max_subscribers: int
    # минимальное количество подписчиков
    min_subscribers: int


@dataclass
class GetDoctorSubscribersResponse:
    # количество подписчиков
    subs_count: int
    # текст "подписчика", "подписчиков", "подписчик"
    subs_count_text: str
    # дата последнего обновления в сервисе
    last_updated_date: str
