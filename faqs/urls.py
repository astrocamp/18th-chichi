from django.urls import path
from . import views

app_name = "faqs"

urlpatterns = [
    path("<slug:slug>", views.show, name="show"),
    path("<slug:slug>/edit", views.edit, name="edit"),
    path("<slug:slug>/delete", views.delete, name="delete"),
    path("updated-faq-position/", views.updated_faq_position, name="updated_faq_position"),
]
