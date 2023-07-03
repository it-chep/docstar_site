import threading
import requests
from .models import GetCourseExportID
from time import sleep

# GETCOURSE CONFIG
secret_key = '5yvK6Jxqvjn0XcLoaZhlEKgWVDi7OcIGoVSkPnV7bikIAtliZe2mekpuhCPlcXz9f6uLrkm67APEfS562u6FzB4SXo6vJy0Oa9qxo9K94M0g5DGRChkjPgZmHdXKYOE5'
account_name = 'readymama'
group_id = 1728991
# GETCOURSE CONFIG


def get_export_id():
    try:
        sleep(60)
        while True:
            print(123)
            # group_id = requests.get(f'https://{account_name}.getcourse.ru/pl/api/account/groups?key={secret_key}')
            # export_id = requests.get(f"https://{account_name}.getcourse.ru/pl/api/account/users?key={secret_key}&status=active") - общий экспорт

            export_id = requests.get(
                f"https://{account_name}.getcourse.ru/pl/api/account/groups/{group_id}/users?key={secret_key}&status=active")  # Экспрот ключа по группе
            # print('export_id', export_id.json())
            # print(export_id.json(), 'export')
            jsonData = export_id.json()['info']

            if jsonData:
                export_id = jsonData['export_id']

            exip = GetCourseExportID()
            exip.export_id = export_id
            exip.save()

            sleep(86400)

    except Exception as e:
        print(e)

