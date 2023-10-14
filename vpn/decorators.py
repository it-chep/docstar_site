import json
from django.http import HttpResponse
from json.decoder import JSONDecodeError


def validate_json_request(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST":
            try:
                data = json.loads(request.body.decode('utf-8'))
            except JSONDecodeError:
                return HttpResponse(status=400,
                                    content='Ошибка в теле json запроса, проверьте его на наличие и целостность данных')
            return view_func(request, data, *args, **kwargs)
        else:
            return HttpResponse(status=403, content='Эндпоинт поддерживает только запросы методом POST')
    return wrapper
