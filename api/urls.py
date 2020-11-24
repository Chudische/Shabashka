from django.urls import path

from .views import offers, OfferDetailView, comments, offer_status

urlpatterns = [
    path('offers/status/<int:pk>', offer_status),
    path('offers/<int:pk>/comments', comments),
    path('offers/<int:pk>/', OfferDetailView.as_view()),
    path('offers/', offers)
]