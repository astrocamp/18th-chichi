from django.shortcuts import render
from projects.models import Project
from django.core.paginator import Paginator
from categories.models import Category


def homepages(request):
    # 獲取頂級分類（沒有父分類的分類）
    categories = Category.objects.filter(parent__isnull=True)

    # 獲取所有專案，預取 categories 及其父分類，並按創建時間降序排列
    projects = Project.objects.prefetch_related("categories__parent").order_by(
        "-created_at"
    )

    return render(
        request,
        "homepages/homepages.html",
        {
            "projects": projects,
            "categories": categories,
        },
    )
