from django.urls import path
from . import views

app_name = "faqs"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("<int:id>", views.show, name="show"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("<int:id>/delete", views.delete, name="delete"),
    path("updated-faq-position/", views.updated_faq_position, name="updated_faq_position"),
]
