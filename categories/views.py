from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from categories.models import Category


@permission_required("categories.view_category", raise_exception=True)
def index(request):
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, "categories/index.html", {"categories": categories})
