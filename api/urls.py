from django.urls import path

from .views import offers, OfferDetailView, comments

urlpatterns = [
    path('offers/<int:pk>/comments', comments),
    path('offers/<int:pk>/', OfferDetailView.as_view()),
    path('offers/', offers)
]