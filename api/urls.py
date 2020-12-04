from django.urls import path

from . import views

urlpatterns = [
    path('offers/status/<int:pk>', views.offer_status),
    path('offers/<int:pk>/comments', views.comments),
    path('offers/<int:pk>/', views.OfferDetailView.as_view()),
    path('offers/', views.offers),
    path('favorite/', views.favorive)
]