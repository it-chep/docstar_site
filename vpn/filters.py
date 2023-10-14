import datetime


def filter_date_from_param(date_param, model):
    today = datetime.date.today()
    if date_param == 'day':
        last_day_start = today - datetime.timedelta(days=1)
        return model.filter(registration_date_time__gte=last_day_start)
    elif date_param == 'week':
        last_week_start = today - datetime.timedelta(days=7)
        return model.filter(registration_date_time__gte=last_week_start)
    elif date_param == '30_days':
        last_month_start = today - datetime.timedelta(days=30)
        return model.filter(registration_date_time__gte=last_month_start)
    elif date_param == 'all':
        return model.filter()
