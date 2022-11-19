from django.contrib import admin
from django.db.models import Sum

from .models import UserIp, DayAnalytics, AllAnalytics

@admin.register(DayAnalytics)
class DayAnalyticsAdmin(admin.ModelAdmin):
    readonly_fields = ('day', 'count', 'count_id')
    list_display = ('day', 'count', 'count_id')
    list_per_page = 10
    


@admin.register(AllAnalytics)
class AllAnalyticsAdmin(admin.ModelAdmin):
    readonly_fields = ('count_all', 'count_all_id')
    list_display = ('count_all', 'count_all_id')

@admin.register(UserIp)
class UserIpAdmin(admin.ModelAdmin):
    list_display = ('ip', )
