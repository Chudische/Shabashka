from django.urls import path
from django.conf import settings


from . import views

app_name ='main'
urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/login/', views.ShaLogin.as_view(), name="login"),
    path('accounts/logout/', views.ShaLogout.as_view(), name='logout'),
    path('accounts/profile/change', views.ChangeProfileView.as_view(), name="profile_change"),
    path('accounts/profile/', views.profile, name="profile"),
    path('accounts/password/change', views.ShaPassChangeView.as_view(), name="password_change"),
    # path('single', views.single, name="single"),
    path('<str:page>/', views.other_page, name="other")

]
