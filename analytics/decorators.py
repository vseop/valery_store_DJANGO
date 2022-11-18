from functools import wraps
from django.db.models import F
from django.db import transaction

from .models import UserIp, DayAnalytics, AllAnalytics


def get_client_ip(request):
    """ Определение IP пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def counted(f):
    """ Cчетчик обычных и уникальных посещений (декоратор) """
    @wraps(f)
    def decorator(request, *args, **kwargs):
        with transaction.atomic():
            counter, _ = DayAnalytics.objects.get_or_create()
            counter_all, _ = AllAnalytics.objects.get_or_create()
            ip = get_client_ip(request)
            if not UserIp.objects.filter(ip=ip):
                UserIp.objects.create(ip=ip)
                counter.count_id = F('count_id') + 1
                counter_all.count_all_id = F('count_all_id') + 1
            counter.count = F('count') + 1
            counter.save()
            counter_all.count_all = F('count_all') + 1
            counter_all.save()
        return f(request, *args, **kwargs)

    return decorator
