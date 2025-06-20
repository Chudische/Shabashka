import datetime

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import ShaUser, SubCategory, SuperCategory, Offer, AdditionalImage, Comment, ShaUserAvatar
from .models import UserReview, ChatMessage, Location 
from .utilities import send_activation_notification
from .forms import SubCategoryForm


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


class SubCategoryInline(admin.TabularInline):
    model = SubCategory


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)


class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class OfferAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'content', 'winner','author', 'created', 'status')
    fields = (('category', 'author', 'status', 'winner'), 'title', 'content', 'price', 'image', 'is_active')
    inlines = (AdditionalImageInline, LocationInline,)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('offer', 'author', 'content', 'price', 'created', 'is_active')
    fields = (('offer', 'author', 'created'), 'content', ('price', 'time_amount', 'measure'), 'is_active')
    readonly_fields = ('created',)


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('offer', 'author', 'reviewal', 'speed', 'cost', 'accuracy', 'content', 'created')
    fields = (('offer', 'author', 'reviewal', 'created'), ('speed', 'cost', 'accuracy'), 'content')
    readonly_fields = ('created',)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('offer', 'author', 'receiver', 'content', 'created')
    feields = ('offer', ('author', 'receiver, created'), 'content')
    readonly_fields = ('created',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('search_id', 'name')

    
# Register your models here.
admin.site.register(ShaUser, ShaUserAdmin)
admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ShaUserAvatar)
admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(Location, LocationAdmin)
