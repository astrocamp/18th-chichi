
from django.urls import path
from .views import index,new,show,edit,delete
from comments.views import index as comment_index, new as comment_new


app_name = "projects"

urlpatterns = [
    path('', index , name = "index" ),
    path('new/', new , name = "new" ),
    path('<int:id>', show , name = "show" ),
    path('<int:id>/edit', edit , name = "edit" ),
    path('<int:id>/delete', delete , name = "delete" ),
    path('<int:id>/comments', comment_index , name = "comment_index" ),
    path('<int:id>/comments/new', comment_new , name = "comment_new" ),




]
