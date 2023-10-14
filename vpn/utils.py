from django.http import HttpResponse


def validate_vpn_save_data_error(e):
    if 'duplicate key value violates unique constraint' in str(e) and 'tg_id_key' in str(e):
        return HttpResponse("Пользователь с таким tg_id уже существует", status=400)
    elif 'duplicate key value violates unique constraint' in str(e) and 'sb_id_key' in str(e):
        return HttpResponse("Пользователь с таким sb_id уже существует", status=400)
    elif 'duplicate key value violates unique constraint' in str(e) and 'gk_id_key' in str(e):
        return HttpResponse("Пользователь с таким gk_id уже существует", status=400)
    else:
        return HttpResponse("Произошла ошибка на стороне сервера", status=500)
