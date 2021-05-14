from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from django.contrib.staticfiles.views import serve



from . import views

app_name ='main'
urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/login/', views.ShaLogin.as_view(), name="login"),
    path('accounts/logout/', views.ShaLogout.as_view(), name='logout'),
    path('accounts/profile/delete', views.DeleteUserView.as_view(), name="profile_delete"),
    path('accounts/profile/change', views.ChangeProfileView.as_view(), name="profile_change"),
    path('accounts/profile/change/<int:pk>/', views.offer_change, name="offer_change"),
    path('accounts/profile/delete/<int:pk>/', views.offer_delete, name="offer_delete"),
    path('accounts/profile/add/', views.add_new_offer, name="add_new_offer"),    
    path('accounts/profile/<int:pk>', views.profile_by_id, name="profile_by_id"),
    path('accounts/profile/', views.profile, name="profile"),
    path('accounts/password/change', views.ShaPassChangeView.as_view(), name="password_change"),
    path('accounts/password/reset/', views.ShaPassResetView.as_view(), name="password_reset"),
    path('accounts/password/reset/done/', views.ShaPassResetDoneView.as_view(), name="password_reset_done"),
    path('accounts/password/reset/confirm/<str:uidb64>/<str:token>/', views.ShaPassResetConfirmView.as_view(), name="password_reset_confirm"),
    path('accounts/password/reset/complete/', views.ShaPassResetCompleteView.as_view(), name="password_reset_complete"),    
    path('accounts/register/activate/<str:sign>/', views.user_activate, name="register_activate"),
    path('accounts/register/done', views.RegisterDone.as_view(), name="register_done"),
    path('accounts/register/', views.RegisterUserView.as_view(), name="register_user"),
    path('accounts/social-auth/', include('social_django.urls', namespace="social")),    
    path('reviews/<int:user_id>', views.reviews, name="reviews"),
    path('user_review/<int:offer_pk>/<int:user_pk>/', views.UserReviewView.as_view(), name="user_review"),   
    path('<int:category_pk>/<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/', views.by_category, name="by_category"),    
    path('chat_list/', views.chat_list, name="chat_list"),
    path('chat/<int:offer_pk>', views.chat, name="chat"),
    path('favorite/', views.favorite, name='favorite'),
    path('<str:page>/', views.other_page, name="other")
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
