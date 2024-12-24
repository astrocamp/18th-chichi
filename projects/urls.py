from django.urls import path
from .views import show, edit, delete, collect_projects, like_projects
from comments.views import index as comment_index, new as comment_new
from faqs.views import index as faq_index, new as faq_new
from update_records.views import (
    index as update_records_index,
    new as update_records_new,
)

app_name = "projects"

urlpatterns = [
    # 移到account urls
    path("<int:id>", show, name="show"),
    path("<int:id>/edit", edit, name="edit"),
    path("<int:id>/delete", delete, name="delete"),
    path("<int:id>/collect", collect_projects, name="collect"),
    path("<int:id>/comments", comment_index, name="comment_index"),
    path("<int:id>/comments/new", comment_new, name="comment_new"),
    path("<int:id>/faq", faq_index, name="faq_index"),
    path("<int:id>/faq/new", faq_new, name="faq_new"),
    path("<int:id>/update_records", update_records_index, name="update_records_index"),
    path("<int:id>/update_records/new", update_records_new, name="update_records_new"),
    path("<int:id>/like", like_projects, name="like"),
]
