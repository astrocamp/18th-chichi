from django.urls import path
from . import views
from projects.views import index,new

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("<int:id>", views.index, name="index"),
    path("<int:id>/projects",index, name="projects"),
    path("<int:id>/projects/new",new, name="projects_new")
]
