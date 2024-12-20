
from django.urls import path
from .views import index,new,show,edit,delete
from faqs.views import index as faq_index, new as faq_new

app_name = "projects"

urlpatterns = [
    path('', index , name = "index" ),
    path('new/', new , name = "new" ),
    path('<int:id>', show , name = "show" ),
    path('<int:id>/edit', edit , name = "edit" ),
    path('<int:id>/delete', delete , name = "delete" ),
    path('<int:id>/faq', faq_index , name = "faq_index" ),
    path('<int:id>/faq/new', faq_new , name = "faq_new" ),
]
