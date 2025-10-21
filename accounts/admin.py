from django.contrib import admin
import datetime

from .models import ShaUser, ShaUserAvatar, Location
from main.utilities import send_activation_notification

def send_activation_notifications(modeladmin, request, queryset):
    """ Sending a messages with activation notification"""
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, "Activation notification letter is sent")
    send_activation_notifications.short_description = 'Sending activation notification letter'


class NonativatedFilter(admin.SimpleListFilter):
    title = 'Activated?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
                    ("activated", "Activated"),
                    ("threedays", "Not activated more than 3 days "),
                    ("week", "Not activated more than a week")
                )

    def queryset(self, request, queryset):        
        if self.value() == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        if self.value() == 'threedays':
            date = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=date)
        if self.value() == 'week':
            date = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=date)


class LocationInline(admin.TabularInline):
    model = Location


class ShaUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonativatedFilter, )
    inlines = (LocationInline, )
    fields = (('username', 'email'), ('first_name', 'last_name'), 'average_rating',
              ('send_message', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'),
              'favorite')
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications, )

admin.site.register(ShaUser, ShaUserAdmin)
admin.site.register(ShaUserAvatar)
admin.site.register(Location)