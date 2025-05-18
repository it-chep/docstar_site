import uuid

from translate import Translator
from docstar_site.models import *


def get_eng_slug(text, src='ru', dest='en') -> str:
    try:
        text = text.lower()
        text = "-".join(text.split(" "))
        translator = Translator(from_lang=src, to_lang=dest)
        translation = translator.translate(text)
        if " " in translation:
            translation = translation.replace(" ", "-")

        return translation

    except Exception as e:
        return str(uuid.uuid4())

def validate_data(data):
    valid_ans = str(data if data != '' else '---')
    return valid_ans


def validate_foreign(city, speciallity, city_list, spec_list):
    if city in city_list:
        return City.objects.get(name=city)

    if speciallity in spec_list:
        return Speciallity.objects.get(name=speciallity)
    return None


def subs_to_str(number):
    try:
        if number == '':
            return 'Нет доступа'
        number = int(number)
        if number <= 1000:
            return number

        elif number < 1000000:
            if str(number // 100 % 10) != '0':
                return str(number // 1000) + '.' + str(number // 100 % 10) + 'к'
            else:
                return str(number // 1000) + 'к'

        elif number >= 1000000:
            if str(number // 100000 % 10) != '0':
                return str(number // 1000000) + '.' + str(number // 100000 % 10) + 'м'
            else:
                return str(number // 1000000) + 'м'
        return None
    except Exception as ex:
        return 0


def get_params(data):
    params = {
        'email': data[1],
        'name': data[5] + '' + data[6],
        'inst_url': validate_data(data[22]),
        'vk_url': validate_data(data[23]),
        'dzen_url': validate_data(data[24]),
        'tg_url': validate_data(data[25]),
        'main_theme': validate_data(data[29]),
        'subs': subs_to_str(data[30]),
        'additional_speciallity': validate_data(data[31]),
        'medical_direcion': validate_data(data[32]),
        'prodoc': validate_data(data[33])
    }

    return params
