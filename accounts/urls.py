from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.ShaLogin.as_view(), name="login"),
    path('logout/', views.ShaLogout.as_view(), name='logout'),
    path('profile/delete', views.DeleteUserView.as_view(), name="profile_delete"),
    path('profile/update', views.ChangeProfileView.as_view(), name="profile_change"),
    path('profile/<int:pk>', views.profile_by_id, name="profile_by_id"),
    path('profile/', views.profile, name="profile"),
    path('password/change', views.ShaPassChangeView.as_view(), name="password_change"),
    path('password/reset/', views.ShaPassResetView.as_view(), name="password_reset"),
    path('password/reset/done/', views.ShaPassResetDoneView.as_view(), name="password_reset_done"),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', views.ShaPassResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password/reset/complete/', views.ShaPassResetCompleteView.as_view(), name="password_reset_complete"),
    path('register/activate/<str:sign>/', views.user_activate, name="register_activate"),
    path('register/done', views.RegisterDone.as_view(), name="register_done"),
    path('register/', views.RegisterUserView.as_view(), name="register_user"),
    path('social-auth/', include('social_django.urls', namespace="social")),
]
