from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from django.contrib.staticfiles.views import serve
from django.contrib.sitemaps.views import sitemap
from .sitemaps import OfferSitemap


from . import views


app_name = 'main'
urlpatterns = [
    path('', views.index, name="index"),
    path('change/<int:pk>/', views.offer_change, name="offer_change"),
    path('delete/<int:pk>/', views.offer_delete, name="offer_delete"),
    path('profile/add/', views.add_new_offer, name="add_new_offer"),
    path('reviews/<int:user_id>', views.reviews, name="reviews"),
    path('user_review/<int:offer_pk>/<int:user_pk>/', views.UserReviewView.as_view(), name="user_review"),
    path('<int:category_pk>/<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/', views.by_category, name="by_category"),
    path('chat_list/', views.chat_list, name="chat_list"),
    path('chat/<int:offer_pk>', views.chat, name="chat"),
    path('favorite/', views.favorite, name='favorite'),
    path('services/', views.services, name='services'),
    path('<str:page>/', views.other_page, name="other"),
    path('sitemap.xml', sitemap, {'sitemaps': {'offer': OfferSitemap}}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
