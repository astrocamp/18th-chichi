from django.shortcuts import render
from projects.models import Project
from django.core.paginator import Paginator
from categories.models import Category


def homepages(request):
    projects = Project.objects.all().order_by("-created_at")
    paginator = Paginator(projects, 12)
    categories = Category.objects.filter(parent=None)
    page = request.GET.get("page")
    projects = paginator.get_page(page)
    return render(
        request,
        "homepages/homepages.html",
        {"projects": projects, "categories": categories},
    )
