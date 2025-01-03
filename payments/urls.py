from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("notify/", views.payment_notify, name="payment_notify"),
    path("complete/", views.payment_complete, name="payment_complete"),
]
