
from django.urls import path
from .views import index,new,show,edit,delete, Collect_projects


app_name = "projects"

urlpatterns = [
    path('', index , name = "index" ),
    path('new/', new , name = "new" ),
    path('<int:id>', show , name = "show" ),
    path('<int:id>/edit', edit , name = "edit" ),
    path('<int:id>/delete', delete , name = "delete" ),
    path('<int:id>/collect', Collect_projects , name = "collect" ),
]
