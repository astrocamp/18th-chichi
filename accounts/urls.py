from django.urls import path
from . import views
from projects.views import index,new
from users.views import profiles_index, profiles_edit,profiles_new

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("<int:id>", views.index, name="index"),
    path("<int:id>/projects",index, name="projects"),
    path("<int:id>/projects/new",new, name="projects_new"),
    path("<int:id>/profiles",profiles_index, name="profiles_index"),
    path("<int:id>/profiles/new",profiles_new, name="profiles_new"),
    path("<int:id>/profiles/edit",profiles_edit, name="profiles_edit"),
]
