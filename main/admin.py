import datetime

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from import_export import resources

from accounts.admin import LocationInline
from .models import SubCategory, SuperCategory, Offer, AdditionalImage, Comment, Category
from .models import UserReview, ChatMessage
from .forms import SubCategoryForm



    




class SubCategoryInline(admin.TabularInline):
    model = SubCategory


class CategoryAdmin(ImportExportModelAdmin):
    model = Category


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)


class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class OfferAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'content', 'winner', 'author', 'created', 'status')
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
admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
