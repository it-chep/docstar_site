from django.core.management.base import BaseCommand
from django.conf import settings

from docstar_site.models import Doctor


class Command(BaseCommand):
    help = 'Перенос фотографий врачей на S3'

    def handle(self, *args, **options):
        s3 = settings.S3_CLIENT

        # доктора
        doctors = Doctor.objects.all()
        total_doctors = doctors.count()

        # каунтеры
        processed = 0
        skipped = 0
        uploaded = 0

        self.stdout.write(self.style.SUCCESS(f'Начало переноса {total_doctors} врачей'))

        for doctor in doctors:
            processed += 1
            avatar = doctor.avatar

            if not avatar:
                self.stdout.write(f'[{processed}/{total_doctors}] Врач {doctor.slug} без фото - пропуск')
                skipped += 1
                continue

            if doctor.s3_image:
                self.stdout.write(
                    f'[{processed}/{total_doctors}] Врач {doctor.slug} уже в S3 ({doctor.s3_image}) - пропуск')
                skipped += 1
                continue

            file_str = avatar.url
            if 'zag' in file_str:
                self.stdout.write(f'[{processed}/{total_doctors}] Врач {doctor.slug} содержит "zag" в URL - пропуск')
                skipped += 1
                continue

            s3_image = f"images/user_{doctor.slug}_{avatar.name.split('/')[-1]}"

            try:
                self.stdout.write(f'[{processed}/{total_doctors}] Загрузка фото врача {doctor.slug}...')
                with open(avatar.path, 'rb') as file_data:
                    s3.put_object(file_data, s3_image)

                doctor.s3_image = s3_image
                doctor.save()

                uploaded += 1
                self.stdout.write(self.style.SUCCESS(f'Успешно: {s3_image}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка у {doctor.slug}: {str(e)}'))

        # Итоговая статистика
        self.stdout.write(self.style.SUCCESS('\nЗавершено!'))
        self.stdout.write(f'Всего врачей: {total_doctors}')
        self.stdout.write(f'Обработано: {processed}')
        self.stdout.write(f'Загружено в S3: {uploaded}')
        self.stdout.write(f'Пропущено: {skipped}')
