from django.shortcuts import render
from categories.models import Category

def index(request):
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, "categories/index.html", {"categories": categories})
