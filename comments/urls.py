
from django.urls import path
from .views import index, new, show, edit, delete


app_name = "comments"

urlpatterns = [
    path('<int:id>/', show , name = "show" ),
    path('<int:id>/edit', edit , name = "edit" ),
    path('<int:id>/delete', delete , name = "delete" ),
]
