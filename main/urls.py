from django.urls import path
from django.conf import settings


from . import views

app_name ='main'
urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/login/', views.ShaLogin.as_view(), name="login"),
    path('accounts/logout/', views.ShaLogout.as_view(), name='logout'),
    path('accounts/profile/delete', views.DeleteUserView.as_view(), name="profile_delete"),
    path('accounts/profile/change', views.ChangeProfileView.as_view(), name="profile_change"),
    path('accounts/profile/', views.profile, name="profile"),
    path('accounts/password/change', views.ShaPassChangeView.as_view(), name="password_change"),
    path('accounts/register/activate/<str:sign>/', views.user_activate, name="register_activate"),
    path('accounts/register/done', views.RegisterDone.as_view(), name="register_done"),
    path('accounts/register/', views.RegisterUserView.as_view(), name="register_user"),
    # path('single', views.single, name="single"),
    path('<int:pk>/', views.by_category, name="by_category"),
    path('<str:page>/', views.other_page, name="other")

]
