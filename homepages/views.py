from django.shortcuts import render
from projects.models import Project
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from categories.models import Category


def homepages(request):
    categories = Category.objects.filter(parent__isnull=True)

    projects = (
        Project.objects.prefetch_related("categories__parent")
        .filter(status="live", deleted_at__isnull=True)
        .order_by("-created_at")
    )

    category = request.GET.get("category")
    if category:
        try:
            category_obj = Category.objects.get(title=category, parent__isnull=True)
            projects = projects.filter(
                categories__in=Category.objects.filter(parent=category_obj)
            ).distinct()
        except Category.DoesNotExist:
            projects = projects.none()

    # 分頁設置
    paginator = Paginator(projects, 12)
    if category and not request.GET.get("page"):
        page_number = 1
    else:
        page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        "homepages/homepages.html",
        {
            "categories": categories,
            "page_obj": page_obj,
            "current_category": category,
        },
    )
