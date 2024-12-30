import datetime
import threading
import time
from collections import defaultdict
from io import BytesIO

from openpyxl import Workbook
from django.core.files.base import ContentFile

import requests
from django.conf import settings
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse

from infrastructure.models import LtvClubReport


@admin.register(LtvClubReport)
class LtvClubReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/ltv_club_report/change_list.html"
    list_display = (
        'export_id',
        'status',
        'date_created',
        'export_time',
    )
    list_filter = (
        'status',
        'date_created',
    )
    search_fields = (
        'export_id',
        'status',
    )
    ordering = ('-date_created',)
    readonly_fields = (
        "report_file",
        'status',
        'export_id',
        'export_time',
        'date_created',
    )

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                'get_ltv_club_report/',
                self.admin_site.admin_view(self.get_ltv_club_report),
                name='get_ltv_club_report',
            ),
            path(
                'get_ltv_last_year_club_report/',
                self.admin_site.admin_view(self.get_ltv_last_year_club_report),
                name='get_ltv_last_year_club_report',
            )
        ]

        return custom_urls + urls

    def get_ltv_last_year_club_report(self, request):
        return self.get_ltv_club_report(request, True)

    def get_ltv_club_report(self, request, current_year: bool = False):
        response = requests.get(
            f"https://{settings.GK_ACCOUNT_NAME}.getcourse.ru/pl/api/account/deals?key={settings.GK_KEY}&user_in_group=4024294&status=payed"
        )
        try:
            jsonData = response.json()
        except Exception:
            self.message_user(
                request=request,
                message="Произошла непредвиденная ошибка",
                level=messages.ERROR
            )
            return redirect(reverse("admin:infrastructure_ltvclubreport_changelist"))

        export_id = None
        if jsonData:
            export_id = jsonData["info"].get('export_id')

        error_message = jsonData["error_message"]
        if error_message:
            self.message_user(
                request=request,
                message=error_message,
                level=messages.ERROR
            )
            return redirect(reverse("admin:infrastructure_ltvclubreport_changelist"))

        if not export_id:
            self.message_user(
                request=request,
                message="Произошла ошибка при создании файла импорта, пожалуйста попробуйте позже",
                level=messages.ERROR
            )
            return redirect(reverse("admin:infrastructure_ltvclubreport_changelist"))

        self.message_user(
            request=request,
            message="Создаю отчет по LTV клуба, пожалуйста ожидайте",
            level=messages.SUCCESS
        )

        ltv_report = LtvClubReport.objects.create(
            export_id=export_id,
        )

        ltv_report_thread = threading.Thread(
            target=self.save_ltv_club_report,
            daemon=True,
            kwargs={
                "ltv_report_id": ltv_report.id,
                "current_year": current_year
            }
        )
        ltv_report_thread.start()

        return redirect(reverse("admin:infrastructure_ltvclubreport_changelist"))

    def save_ltv_club_report(self, *args, **kwargs):
        ltv_report_id = kwargs.get('ltv_report_id')
        current_year = kwargs.get('current_year')
        ltv_report = LtvClubReport.objects.filter(id=ltv_report_id).first()

        if not ltv_report:
            raise ValueError("Отчет с указанным ID не найден")

        export_id = ltv_report.export_id
        ltv_report.status = 'Pending'
        ltv_report.save()

        while True:
            try:
                response = requests.get(
                    f'https://{settings.GK_ACCOUNT_NAME}.getcourse.ru/pl/api/account/exports/{export_id}?key={settings.GK_KEY}'
                )
                data = response.json()
                if response.status_code == 200 and data["error"] is False:
                    break
                time.sleep(60)

            except Exception as e:
                ltv_report.status = 'Error'
                ltv_report.save()
                raise e

        items = data["info"]['items']
        self.generate_xlsx_report(ltv_report, items, current_year)

    @staticmethod
    def generate_xlsx_report(ltv_report: LtvClubReport, items: list, current_year: bool = False):
        try:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "LTV Club Report"

            headers = ["Email", "Количество заказов", "Сумма заказов (RUB)"]
            worksheet.append(headers)

            user_orders = defaultdict(lambda: {"count": 0, "total": 0.0})

            for item in items:
                email = item[4]
                time_start = item[6]
                title = item[8]
                cost = float(item[10])

                date_obj = datetime.datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")
                year = date_obj.year
                if current_year and year != datetime.datetime.now().year:
                    continue

                if cost < 100:
                    continue

                if "клуб" in title.lower():
                    user_orders[email]["count"] += 1
                    user_orders[email]["total"] += cost

            for email, data in user_orders.items():
                worksheet.append([email, data["count"], data["total"]])

            file_buffer = BytesIO()
            workbook.save(file_buffer)
            file_buffer.seek(0)

            ltv_report.report_file.save(
                f"ltv_club_report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx",
                ContentFile(file_buffer.read())
            )
            file_buffer.close()

            ltv_report.status = 'Completed'
            ltv_report.save()

        except Exception as e:
            ltv_report.status = 'Error'
            ltv_report.save()
            raise e
