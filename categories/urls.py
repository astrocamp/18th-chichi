from django.urls import path
from .views import index

app_name = "categories"

urlpatterns = [
    path('', index, name='index'),
]