from django.urls import path
from .views import index,new,show,edit,delete


app_name = "update_records"

urlpatterns = [
    path('', index , name = "index" ),
    path('new/', new , name = "new" ),
    path('<int:id>', show , name = "show" ),
    path('<int:id>/edit', edit , name = "edit" ),
    path('<int:id>/delete', delete , name = "delete" ),
]
