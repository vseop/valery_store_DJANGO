from django.db import models


class UserIp(models.Model):
    """Уникальные Ip адреса"""
    ip = models.CharField(verbose_name='IP адрес', max_length=50)

    class Meta:
        verbose_name = "Уникальные IP"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


class DayAnalytics(models.Model):
    """ Статистика простых и уникальных просмотров за 1 день """

    day = models.DateField(auto_now_add=True, verbose_name='Дата')
    count = models.PositiveIntegerField(verbose_name='Колисество просмотров', default=0)
    count_id = models.PositiveIntegerField(verbose_name='Колисество уникальных посещений', default=0)

    class Meta:
        verbose_name = 'Статистика ежедневных просмотров'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)


class AllAnalytics(models.Model):
    """ Всего просмотров и посещений"""
    count_all = models.PositiveIntegerField(verbose_name='Всего просмотров сайта', default=0)
    count_all_id = models.PositiveIntegerField(verbose_name='Всего уникальных посещений', default=0)

    class Meta:
        verbose_name = 'Статистика за все время'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Уникальные посещения {self.count_all_id}, просмотры {self.count_all}'
