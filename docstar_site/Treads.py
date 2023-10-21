import threading
import requests
from docstar_site.models import GetCourseExportID
from time import sleep
from django.conf import settings


def get_export_id():
    try:
        sleep(60)
        while True:
            # Экспрот ключа по группе
            export_id = requests.get(
                f"https://{settings.GK_ACCOUNT_NAME}.getcourse.ru/pl/api/account/groups/{settings.GK_GROUP_ID}/users?key={settings.GK_KEY}&status=active")
            jsonData = export_id.json()['info']

            if jsonData:
                export_id = jsonData['export_id']

            exip = GetCourseExportID()
            exip.export_id = export_id
            exip.save()

            sleep(86400)

    except Exception as e:
        print(e)
