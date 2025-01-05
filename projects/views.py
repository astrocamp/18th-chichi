from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProjectFrom
from .models import Project, CollectProject, FavoritePrject
from django.utils.timezone import localtime, now
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from comments.models import Comment
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count
from django.utils.timezone import make_aware
import random
from datetime import date,timedelta
from django.db.models import Min, Max, Avg, Q
from decimal import Decimal



from datetime import datetime


def calculate_total_days(end_date):
    """計算到結束日期的總天數"""
    if not end_date:
        return 0
    current_date = now()
    if current_date > end_date:
        return 0
    time_difference = end_date - current_date
    return time_difference.days + 1  # +1 是因為要包含今天


def calculate_progress_percentage(raised_amount, goal_amount):
    """計算達成率"""
    if not goal_amount or goal_amount == 0:
        return 0
    percentage = (raised_amount or 0) / goal_amount * 100
    # 確保百分比不超過 100%
    return min(round(percentage, 1), 100)  # 四捨五入到小數點第一位，並限制最大值為 100


from categories.models import Category


@login_required
def index(request):
    account = request.user
    if request.POST:
        form = ProjectFrom(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.account = account
            project.save()
            return redirect("projects:show", slug=project.slug)
        else:
            return HttpResponse(f"輸入錯誤: {form.errors}")
    projects = Project.objects.filter(account=account)
    media_type = None

    for project in projects:
        project.update_status()
        project.update_raised_amount()  # 更新已籌金額
        # 計算並限制進度百分比
        if project.goal_amount and project.goal_amount > 0:
            project.progress_percentage = min(
                (project.raised_amount or 0) / project.goal_amount * 100, 100
            )
        else:
            project.progress_percentage = 0
        media_type = get_media_type(project.cover_image.name)

    return render(
        request,
        "projects/index.html",
        {"projects": projects, "account": account, "media_type": media_type},
    )


@login_required
def new(request):
    account = request.user
    categories = Category.objects.filter(parent__isnull=True)
    return render(
        request, "projects/new.html", {"account": account, "categories": categories}
    )


@login_required
def show(request, slug):
    project = get_object_or_404(Project, slug=slug)
    account = get_object_or_404(User, id=request.user.id)
    comments = project.comments.filter(parent__isnull=True).order_by("-id")

    # 計算達成率
    progress_percentage = calculate_progress_percentage(
        project.raised_amount, project.goal_amount
    )

    if request.POST:
        # 處理上架邏輯
        if "publish" in request.POST:  # 檢查是否點擊了上架按鈕
            if project.status == "pending":
                project.status = "live"  # 將狀態改為已上架
                project.start_at = timezone.now()  # 更新 start_at 為當前時間
                project.save()
                messages.success(request, "已上架")

                return redirect("projects:show", slug=project.slug)
        elif "unpublish" in request.POST:
            if project.status == "live":
                project.status = "ended"  # 將狀態改為已上架
                project.end_at = timezone.now()  # 更新 start_at 為當前時間
                project.save()
                messages.success(request, "已下架")

                return redirect("projects:show", slug=project.slug)

        else:
            form = ProjectFrom(request.POST, request.FILES, instance=project)
            form.save()
            project.update_at = timezone.now()
            project.save()
            return redirect("projects:show", slug=project.slug)

        return redirect("projects:show", slug=project.slug)

    collected = CollectProject.objects.filter(
        account=request.user, project=project
    ).first()

    favorited = FavoritePrject.objects.filter(
        account=request.user, project=project
    ).first()

    media_type = get_media_type(project.cover_image.name)
    return render(
        request,
        "projects/show.html",
        {
            "project": project,
            "collected": collected,
            "account": account,
            "favorited": favorited,
            "comments": comments,
            "media_type": media_type,
            "progress_percentage": progress_percentage,  # 加入達成率
        },
    )


def comment(request, slug):
    project = get_object_or_404(Project, slug=slug)
    account = get_object_or_404(User, id=request.user.id)
    comments = project.comments.filter(parent__isnull=True).order_by("-id")
    return render(
        request,
        "projects/comment.html",
        {"project": project, "account": account, "comments": comments},
    )


def get_media_type(file_name):
    file_name = file_name.lower()
    image_extensions = (".jpg", ".jpeg", ".png", ".gif")
    video_extensions = (".mp4", ".mov", ".avi", ".wmv")

    if file_name.endswith(image_extensions):
        return "image"
    elif file_name.endswith(video_extensions):
        return "video"
    return "unsupported"


@login_required
def edit(request, slug):
    project = get_object_or_404(Project, slug=slug)
    media_type = get_media_type(project.cover_image.name)

    format_time_start = localtime(project.start_at).strftime("%Y-%m-%dT%H:%M")
    format_time_end = localtime(project.end_at).strftime("%Y-%m-%dT%H:%M")
    return render(
        request,
        "projects/edit.html",
        {
            "project": project,
            "format_time_start": format_time_start,
            "format_time_end": format_time_end,
            "media_type": media_type,
        },
    )


@login_required
def delete(request, slug):
    # 獲取專案並確保是當前用戶的專案
    project = get_object_or_404(Project, slug=slug, account=request.user)

    if request.POST:
        project.delete()
        messages.success(request, "專案已成功刪除")
        return redirect("projects:index")

    return render(request, "projects/delete.html", {"project": project})


@login_required
@require_POST
def collect_projects(request, slug):
    project = get_object_or_404(Project, slug=slug)
    collect, created = CollectProject.objects.get_or_create(
        account=request.user,
        project=project,
    )

    if not created:
        collect.delete()

    # 根據來源頁面決定重定向目標
    referer = request.META.get("HTTP_REFERER", "")
    if "public" in referer:
        return redirect("projects:public", slug=project.slug)
    return redirect("projects:show", slug=project.slug)


@login_required
@require_POST
def like_projects(request, slug):
    project = get_object_or_404(Project, slug=slug)
    favorite, created = FavoritePrject.objects.get_or_create(
        account=request.user,
        project=project,
    )

    if not created:
        favorite.delete()

    # 根據來源頁面決定重定向目標
    referer = request.META.get("HTTP_REFERER", "")
    if "public" in referer:
        return redirect("projects:public", slug=project.slug)
    return redirect("projects:show", slug=project.slug)


def chart_page(request, slug):
    project = get_object_or_404(Project, slug=slug)

    return render(
        request, "projects/chart_page.html", {"slug": slug, "project": project}
    )


@login_required
def gender_proportion(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)

    gender_data = (
        Sponsor.objects.filter(project=project)
        .values("account__profile__gender")
        .annotate(count=Count("id"))
    )

    labels = []
    data = []
    total_count = 0

    for entry in gender_data:
        gender = entry["account__profile__gender"]
        if gender == "M":
            labels.append("男")
        elif gender == "F":
            labels.append("女")
        elif gender == "O":
            labels.append("其他")
        else:
            labels.append("未知")
        count = entry["count"]
        data.append(count)
        total_count += count

    response_data = {
        "labels": labels,
        "datasets": [
            {
                "label": f"贊助者性別比例（總人數: {total_count}）",
                "backgroundColor": ["#F8AFAF", "#FFE69B", "#A8D3F0", "#CACACA"],
                "borderColor": "#FFFFFF",
                "borderWidth": 2,
                "data": data,
            }
        ],
    }

    return JsonResponse(response_data)


@login_required
def daily_sponsorship_amount(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)
    sponsors = Sponsor.objects.filter(project=project)
    if not sponsors.exists():
        return JsonResponse(
            {
                "labels": [],
                "datasets": [
                    {
                        "label": "Cumulative Amount",
                        "backgroundColor": "rgba(75, 192, 192, 0.2)",
                        "borderColor": "rgba(75, 192, 192, 1)",
                        "borderWidth": 2,
                        "data": [],
                    }
                ],
            }
        )

    start_date = sponsors.order_by("created_at").first().created_at.date()
    end_date = sponsors.order_by("-created_at").first().created_at.date()

    daily_totals = {}

    for sponsor in sponsors:
        date = sponsor.created_at.date()
        if date not in daily_totals:
            daily_totals[date] = 0
        daily_totals[date] += sponsor.amount

    date_range = []
    cumulative_amount = []
    cumulative_total = 0

    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        daily_amount = daily_totals.get(current_date, 0)
        cumulative_total += daily_amount
        cumulative_amount.append(cumulative_total)
        current_date += timedelta(days=1)

    data = {
        "labels": [date.strftime("%Y-%m-%d") for date in date_range],
        "datasets": [
            {
                "label": "每日累積金額",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 2,
                "data": cumulative_amount,
            }
        ],
    }

    return JsonResponse(data)


@login_required
def gender_amount_boxplot(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)

    gender_data = (
        Sponsor.objects.filter(project=project, reward__isnull=True)
        .select_related("account__profile")
        .values("account__profile__gender", "amount")
    )

    gender_amounts = {"M": [], "F": [], "O": []}

    for entry in gender_data:
        gender = entry["account__profile__gender"]
        amount = entry["amount"]
        if gender in gender_amounts:
            gender_amounts[gender].append(amount)

    boxplot_data = []
    for gender, amounts in gender_amounts.items():
        if amounts:
            sorted_amounts = sorted(amounts)
            n = len(sorted_amounts)

            q1_idx = int(n * 0.25)
            q2_idx = int(n * 0.5)
            q3_idx = int(n * 0.75)

            q1 = sorted_amounts[q1_idx]
            median = sorted_amounts[q2_idx]
            q3 = sorted_amounts[q3_idx]

            iqr = q3 - q1

            lower_bound = max(min(sorted_amounts), q1 - iqr * Decimal("1.5"))
            upper_bound = min(max(sorted_amounts), q3 + iqr * Decimal("1.5"))

            outliers = [x for x in sorted_amounts if x < lower_bound or x > upper_bound]

            boxplot_data.append(
                {
                    "min": float(lower_bound),
                    "q1": float(q1),
                    "median": float(median),
                    "q3": float(q3),
                    "max": float(upper_bound),
                    "outliers": [float(x) for x in outliers],
                }
            )
        else:
            boxplot_data.append(
                {"min": 0, "q1": 0, "median": 0, "q3": 0, "max": 0, "outliers": []}
            )

    response_data = {
        "labels": ["男", "女", "其他"],
        "datasets": [
            {
                "label": "贊助金額分布",
                "data": boxplot_data,
                "backgroundColor": ["#F8AFAF", "#A8D3F0", "#FFE69B"],
                "borderColor": "#FFFFFF",
                "borderWidth": 2,
            }
        ],
    }

    return JsonResponse(response_data)


@login_required
def reward_grouped_bar_chart(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)

    def get_age_group(birthday):
        if not birthday:
            return None
        age = (date.today() - birthday).days // 365
        if age < 18:
            return "未成年"
        elif 18 <= age <= 25:
            return "18-25"
        elif 26 <= age <= 35:
            return "26-35"
        elif 36 <= age <= 45:
            return "36-45"
        else:
            return "46+"

    sponsor_data = (
        Sponsor.objects.filter(project=project, reward__isnull=False)
        .select_related("reward", "account__profile")
        .values(
            "reward__title", "account__profile__gender", "account__profile__birthday"
        )
        .annotate(count=Count("id"))
        .order_by("reward__title")
    )

    gender_groups = ["M", "F", "O"]
    age_groups = ["未成年", "18-25", "26-35", "36-45", "46+"]

    grouped_data = {}
    for entry in sponsor_data:
        reward_title = entry["reward__title"] or "無回饋"
        gender = entry["account__profile__gender"]
        age_group = get_age_group(entry["account__profile__birthday"])

        if not gender or not age_group:
            continue

        group_key = f"{gender}_{age_group}"
        count = entry["count"]

        if reward_title not in grouped_data:
            grouped_data[reward_title] = {
                f"{g}_{a}": 0 for g in gender_groups for a in age_groups
            }

        grouped_data[reward_title][group_key] = count

    all_combinations = [
        f"{gender}_{age}" for gender in gender_groups for age in age_groups
    ]

    labels = list(grouped_data.keys())
    datasets = []

    colors = {
        "M_18-25": "#4E79A7",
        "M_26-35": "#76B7B2",
        "M_36-45": "#59A14F",
        "M_46+": "#8CD17D",
        "M_未成年": "#A0CBE8",
        "F_18-25": "#F28E2B",
        "F_26-35": "#FF9DA7",
        "F_36-45": "#E15759",
        "F_46+": "#FFB4A2",
        "F_未成年": "#FFB4A2",
        "O_18-25": "#9C755F",
        "O_26-35": "#BAB0AC",
        "O_36-45": "#808080",
        "O_46+": "#666666",
        "O_未成年": "#CCCCCC",
    }

    for combination in all_combinations:
        dataset = {
            "label": combination,
            "backgroundColor": colors.get(
                combination, f"#{random.randint(0, 0xFFFFFF):06x}"
            ),
            "borderColor": "#FFFFFF",
            "borderWidth": 1,
            "data": [grouped_data[reward].get(combination, 0) for reward in labels],
        }
        if any(dataset["data"]):
            datasets.append(dataset)

    response_data = {
        "labels": labels,
        "datasets": datasets,
    }

    return JsonResponse(response_data)


def public(request, slug):
    """
    公開的專案頁面，不需要登入即可查看
    """
    project = get_object_or_404(Project, slug=slug)

    # 計算專案相關數據
    project.update_status()  # 更新專案狀態
    project.update_raised_amount()  # 更新已籌金額

    # 計算總剩餘天數
    total_days = calculate_total_days(project.end_at)

    # 計算達成率
    progress_percentage = calculate_progress_percentage(
        project.raised_amount, project.goal_amount
    )

    # 算贊助人數
    try:
        backers_count = project.get_backers_count()
    except:
        from .models import Sponsor

        backers_count = (
            Sponsor.objects.filter(project=project, status="paid")
            .values("account")
            .distinct()
            .count()
        )

    # 如果用戶已登入，檢查是否已收藏和按讚
    collected = None
    favorited = None
    if request.user.is_authenticated:
        collected = CollectProject.objects.filter(
            account=request.user, project=project
        ).exists()
        favorited = FavoritePrject.objects.filter(
            account=request.user, project=project
        ).exists()

    context = {
        "project": project,
        "total_days": total_days,
        "progress_percentage": progress_percentage,
        "collected": collected,
        "favorited": favorited,
        "backers_count": backers_count,
    }

    return render(request, "projects/public.html", context)


def comments_index(request, slug):
    """
    顯示專案的留言列表，整合 comments app 的功能
    """
    project = get_object_or_404(Project, slug=slug)

    # 獲取主留言（沒有父留言的留言）
    comments = (
        Comment.objects.filter(project=project, parent__isnull=True)
        .order_by("-created_at")
        .select_related("account")
        .prefetch_related("replies", "replies__account")
    )

    if request.method == "DELETE":
        if not request.user.is_authenticated:
            return HttpResponse("請先登入", status=401)

        comment_id = request.GET.get("comment_id")
        if comment_id:
            comment = get_object_or_404(Comment, id=comment_id, project=project)
            if request.user == comment.account:
                comment.delete()
                messages.success(request, "留言已刪除")
            else:
                return HttpResponse("您沒有權限刪除這則留言", status=403)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "請先登入")
            return redirect("projects:comments_index", slug=project.slug)

        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")

        if content:
            # 如果有 parent_id，表示這是一個回覆
            if parent_id:
                parent_comment = get_object_or_404(
                    Comment, id=parent_id, project=project
                )
                Comment.objects.create(
                    project=project,
                    content=content,
                    account=request.user,
                    parent=parent_comment,
                )
                messages.success(request, "回覆成功")
            else:
                # 這是一個主留言
                Comment.objects.create(
                    project=project, content=content, account=request.user
                )
                messages.success(request, "留言成功")

    # 如果是 htmx 請求，返回部分模板
    if request.headers.get("HX-Request"):
        return render(
            request,
            "projects/partials/comments_content.html",
            {"comments": comments, "project": project, "user": request.user},
        )

    return render(
        request,
        "projects/comments.html",
        {"comments": comments, "project": project, "user": request.user},
    )


def get_subcategories(request):
    parent_id = request.GET.get("parent_id")
    if parent_id:
        subcategories = Category.objects.filter(parent_id=parent_id).values(
            "id", "title"
        )
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)
