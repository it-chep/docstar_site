import csv
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from docstar_site.models import Doctor
from docstar_site.utils import validate_inst_url


class Command(BaseCommand):
    help = 'Перенос врачей инсты в базу subscribers'

    def handle(self, *args, **options):
        doctors = Doctor.objects.filter(is_active=True, inst_url__isnull=False)
        total_doctors = doctors.count()
        processed = 0
        skipped = 0

        client = settings.SUBSCRIBERS_CLIENT

        # Создаем CSV файл для логирования
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f'doctors_migration_inst_{timestamp}.csv'

        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = [
                'doctor_id',
                'doctor_name',
                'tg_channel_url',
                'tg_personal_url',
                'instagram_url',
                'status',
                'error_message'
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            self.stdout.write(self.style.SUCCESS(f'Начало переноса {total_doctors} врачей'))
            self.stdout.write(self.style.SUCCESS(f'Логи будут записаны в файл: {csv_filename}'))

            for doctor in doctors:

                time.sleep(1)

                row = {
                    'doctor_id': doctor.id,
                    'doctor_name': doctor.name,
                    'tg_channel_url': doctor.tg_channel_url or '',
                    'tg_personal_url': doctor.tg_url or '',
                    'instagram_url': doctor.inst_url or '',
                    'status': '',
                    'error_message': ''
                }

                try:
                    if doctor.inst_url:
                        inst_username = validate_inst_url(doctor.inst_url)
                        status = client.migrate_instagram(doctor.id, inst_username)
                        if status == 200:
                            row['status'] = 'SUCCESS'
                            self.stdout.write(self.style.SUCCESS(f'Успешно перенес врача - {doctor.id}: {doctor.name}'))
                            processed += 1
                        elif status == 201:
                            row['status'] = 'UPDATED'
                            self.stdout.write(self.style.SUCCESS(f'Успешно обновил врача - {doctor.id}: {doctor.name}'))
                            processed += 1
                        else:
                            row['status'] = 'FAILED'
                            row['error_message'] = 'Не удалось создать врача (канал)'
                            self.stdout.write(self.style.ERROR(
                                f'Не удалось создать врача в SUBSCRIBERS - {doctor.id}: {doctor.name}'))
                            skipped += 1

                except Exception as e:
                    row['status'] = 'ERROR'
                    row['error_message'] = str(e)
                    self.stdout.write(self.style.ERROR(f'Ошибка при обработке врача {doctor.id}: {str(e)}'))
                    skipped += 1

                writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(f'Закончил перенос. УСПЕХ - {processed}, СКИП - {skipped}'))
        self.stdout.write(self.style.SUCCESS(f'Подробный отчет сохранен в: {csv_filename}'))
