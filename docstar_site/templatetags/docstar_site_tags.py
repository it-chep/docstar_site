import json

from django import template
import requests
register = template.Library()


# @register.simple_tag()
# def gk_api():
#     secret_key = '5yvK6Jxqvjn0XcLoaZhlEKgWVDi7OcIGoVSkPnV7bikIAtliZe2mekpuhCPlcXz9f6uLrkm67APEfS562u6FzB4SXo6vJy0Oa9qxo9K94M0g5DGRChkjPgZmHdXKYOE5'
#     account_name = 'readymama'
#     export_id = requests.get(f"https://{account_name}.getcourse.ru/pl/api/account/users?key={secret_key}&status=active")
#     print('export_id', export_id.json())
#     jsonData = export_id.json()['info']
#     if jsonData:
#         id = jsonData['export_id']
#         return id