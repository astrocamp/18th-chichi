from django.urls import path
from .views import index,new,show,edit,delete


app_name = "update_records"

urlpatterns = [
    # 移到projects urls
    path('<int:update_id>', show , name = "show" ),
    path('<int:update_id>/edit', edit , name = "edit" ),
    path('<int:update_id>/delete', delete , name = "delete" ),
]
