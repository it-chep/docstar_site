from django.db import models


class LtvClubReport(models.Model):
    REPORT_STATUS_CHOICES = (
        ('Created', 'Созданный'),
        ('Pending', 'В процессе'),
        ('Error', 'Ошибка'),
        ('Completed', 'Завершен')
    )

    status = models.CharField(
        max_length=40,
        choices=REPORT_STATUS_CHOICES,
        default='Created',
        verbose_name='Статус создания отчета',
    )

    report_file = models.FileField(
        upload_to='ltv_club_reports',
        blank=True,
        null=True,
        verbose_name="Файл с отчетами"
    )

    date_created = models.DateField(
        verbose_name="Дата создания отчета",
        auto_now_add=True
    )

    export_id = models.CharField(
        verbose_name="Export_id",
        max_length=40,
        unique=True,
    )

    export_time = models.DateTimeField(
        verbose_name="Время экспорта",
        auto_now=True,
    )

    def __str__(self):
        return self.export_id

    class Meta:
        verbose_name = 'Отчет по LTV клуба'
        verbose_name_plural = 'Отчеты по LTV клуба'
