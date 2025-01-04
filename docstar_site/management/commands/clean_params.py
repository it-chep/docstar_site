from django.core.management.base import BaseCommand

from docstar_site.models import Doctor


class Command(BaseCommand):
    help = "Clean doctors params"

    def handle(self, *args, **options):
        doctors = Doctor.objects.all()
        for doctor in doctors:
            if doctor.additional_speciallity == "---":
                doctor.additional_speciallity = None
            if doctor.inst_url == "---":
                doctor.inst_url = None
            if doctor.vk_url == "---":
                doctor.vk_url = None
            if doctor.dzen_url == "---":
                doctor.dzen_url = None
            if doctor.tg_url == "---":
                doctor.tg_url = None
            if doctor.prodoctorov == "---":
                doctor.prodoctorov = None
            if doctor.subscribers_inst == "---":
                doctor.subscribers_inst = None
            if doctor.medical_directions == "---":
                doctor.medical_directions = None
            if doctor.main_blog_theme == "---":
                doctor.main_blog_theme = None

            doctor.save()
