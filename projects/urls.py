
from django.urls import path
from .views import show,edit,delete


app_name = "projects"

urlpatterns = [
    # 移到account urls
    path('<int:id>', show , name = "show" ),
    path('<int:id>/edit', edit , name = "edit" ),
    path('<int:id>/delete', delete , name = "delete" ),



]
