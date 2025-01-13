import requests
from django.core.management.base import BaseCommand
from docstar_site.models import Doctor


class Command(BaseCommand):
    help = 'Проверка и корректировка ссылок у врачей'

    def handle(self, *args, **options):
        doctors = Doctor.objects.all()

        for doctor in doctors:
            inst_url = doctor.inst_url
            if inst_url and inst_url != "---" and inst_url != "-":
                if inst_url.startswith("@"):
                    inst_url = inst_url[1:]
                    inst_url = "https://instagram.com/" + inst_url
                if self.is_valid_url(inst_url):
                    doctor.inst_url = inst_url

            vk_url = doctor.vk_url
            if vk_url and vk_url != "---" and vk_url != "-":
                if vk_url.startswith("@"):
                    vk_url = vk_url[1:]
                    vk_url = "https://vk.com/" + vk_url
                if self.is_valid_url(vk_url):
                    doctor.vk_url = vk_url

            tg_url = doctor.tg_url
            if tg_url and tg_url != "---" and tg_url != "-":
                if tg_url.startswith("@"):
                    tg_url = tg_url[1:]
                    tg_url = "https://t.me/" + tg_url
                if self.is_valid_url(tg_url):
                    doctor.tg_url = tg_url

            dzen_url = doctor.dzen_url
            if dzen_url and not self.is_valid_url(dzen_url):
                print(f"Невалидная ссылка Яндекс.Дзен: {dzen_url}")

            prodoctorov_url = doctor.prodoctorov
            if not prodoctorov_url or not self.is_valid_url(prodoctorov_url):
                doctor.prodoctorov = inst_url

            doctor.save()

    def is_valid_url(self, url):
        """Проверка валидности ссылки с помощью HTTP-запроса."""
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
