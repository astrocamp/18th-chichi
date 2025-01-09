from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("", views.index, name="index"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
]
