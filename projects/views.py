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
from datetime import date, timedelta
from django.db.models import Min, Max, Avg, Q
from decimal import Decimal
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from categories.models import Category
from chats.models import ChatRoom, Message
import pandas as pd

from .forms import ProjectSearchForm


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
    return round(percentage)  # 四捨五入到整數


@login_required
def index(request):
    account = request.user
    if request.POST:
        form = ProjectFrom(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.account = account
            project.save()
            project.categories.add(form.cleaned_data["categories"][0])
            return redirect("projects:show", slug=project.slug)
        else:
            return HttpResponse(f"輸入錯誤: {form.errors}")
    projects = Project.objects.filter(account=account, deleted_at__isnull=True)

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

    return render(
        request,
        "projects/index.html",
        {"projects": projects, "account": account},
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
    from .models import ProjectCategory

    account = request.user
    project = get_object_or_404(
        Project, slug=slug, deleted_at__isnull=True, account=account
    )
    comments = project.comments.filter(
        parent__isnull=True,
    ).order_by("-id")

    # 計算達成率
    if project.goal_amount and project.goal_amount > 0:
        progress_percentage = round(
            (project.raised_amount or 0) / project.goal_amount * 100, 1
        )
    else:
        progress_percentage = 0

    # 計算剩餘天數
    total_days = calculate_total_days(project.end_at)

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

    categories = Category.objects.filter(
        id__in=ProjectCategory.objects.filter(project_id=project.id).values_list(
            "category_id", flat=True
        )
    )

    parent_ids = [category.parent_id for category in categories if category.parent_id]
    parent_categories = Category.objects.filter(id__in=parent_ids)

    # 獲取聊天室列表
    chat_rooms = ChatRoom.objects.filter(project=project).order_by("-updated_at")
    for room in chat_rooms:
        # 獲取最後一條消息
        last_message = (
            Message.objects.filter(chat_room=room).order_by("-created_at").first()
        )
        room.last_message = last_message
        # 獲取未讀消息數量
        room.unread_count = Message.objects.filter(
            chat_room=room, is_read=False, sender=room.visitor
        ).count()

    return render(
        request,
        "projects/show.html",
        {
            "project": project,
            "collected": collected,
            "account": account,
            "favorited": favorited,
            "comments": comments,
            "progress_percentage": progress_percentage,  # 加入達成率
            "total_days": total_days,  # 加入剩餘天數
            "categories": categories,
            "parent_categories": parent_categories,
            "chat_rooms": chat_rooms,  # 加入聊天室列表
        },
    )


def comment(request, slug):
    account = get_object_or_404(User, id=request.user.id)
    project = get_object_or_404(Project, slug=slug, account=account)
    comments = project.comments.filter(parent__isnull=True).order_by("-id")
    return render(
        request,
        "projects/comment.html",
        {"project": project, "account": account, "comments": comments},
    )


@login_required
def edit(request, slug):
    from .models import ProjectCategory

    account = get_object_or_404(User, id=request.user.id)
    project = get_object_or_404(Project, slug=slug, account=account)

    # 找出專案相關的子分類
    categories = Category.objects.filter(
        id__in=ProjectCategory.objects.filter(project_id=project.id).values_list(
            "category_id", flat=True
        )
    )

    # 找出所有父分類
    parent_ids = [category.parent_id for category in categories if category.parent_id]
    all_parent_categories = Category.objects.filter(parent__isnull=True)
    parent_categories = Category.objects.filter(id__in=parent_ids)

    # 取得已選中的主要分類與子分類
    selected_sub_category = categories.first() if categories.exists() else None
    selected_category = selected_sub_category.parent if selected_sub_category else None

    return render(
        request,
        "projects/edit.html",
        {
            "account": account,
            "project": project,
            "all_parent_categories": all_parent_categories,  # 所有父分類
            "categories": parent_categories,  # 傳遞父分類到模板
            "selected_category": selected_category,  # 預設選中的主要分類
            "selected_sub_category": selected_sub_category,  # 預設選中的子分類
        },
    )


@login_required
def delete(request, slug):
    # 獲取專案並確保是當前用戶的專案
    project = get_object_or_404(Project, slug=slug, account=request.user)

    if request.POST:
        project.deleted_at = timezone.now()
        project.save()
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
        collected = False
    else:
        collected = True

    return JsonResponse(
        {
            "collected": collected,
            "collect_count": project.get_collect_count(),
        }
    )


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
        favorited = False
    else:
        favorited = True

    return JsonResponse(
        {
            "favorited": favorited,
            "like_count": project.get_like_count(),
        }
    )


def chart_page(request, slug):
    project = get_object_or_404(Project, slug=slug, account=request.user)

    return render(
        request, "projects/chart_page.html", {"slug": slug, "project": project}
    )


@login_required
def gender_proportion(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)

    # 使用 distinct() 確保只計算唯一贊助者
    gender_data = (
        Sponsor.objects.filter(project=project)
        .values("account__profile__gender")
        .distinct()
        .annotate(count=Count("account", distinct=True))
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
def gender_amount_scatter(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)

    gender_data = (
        Sponsor.objects.filter(project=project, reward__isnull=True)
        .select_related("account__profile")
        .values("account__profile__gender", "amount")
    )

    scatter_data = {"M": [], "F": [], "O": []}
    median_data = {"M": 0, "F": 0, "O": 0}

    # 將數據分類
    for entry in gender_data:
        gender = entry["account__profile__gender"]
        amount = entry["amount"]
        if gender in scatter_data:
            scatter_data[gender].append(float(amount))

    # 計算中位數
    for gender, amounts in scatter_data.items():
        if amounts:
            sorted_amounts = sorted(amounts)
            n = len(sorted_amounts)
            if n % 2 == 0:
                median_data[gender] = (
                    sorted_amounts[n // 2 - 1] + sorted_amounts[n // 2]
                ) / 2
            else:
                median_data[gender] = sorted_amounts[n // 2]

    response_data = {
        "labels": ["男", "女", "其他"],
        "scatter_datasets": [
            {
                "label": "男",
                "data": scatter_data["M"],
                "backgroundColor": "#F8AFAF",
            },
            {
                "label": "女",
                "data": scatter_data["F"],
                "backgroundColor": "#A8D3F0",
            },
            {
                "label": "其他",
                "data": scatter_data["O"],
                "backgroundColor": "#FFE69B",
            },
        ],
        "median_data": [
            {"x": "男", "y": median_data["M"]},
            {"x": "女", "y": median_data["F"]},
            {"x": "其他", "y": median_data["O"]},
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
    from .models import ProjectCategory, Sponsor

    project = get_object_or_404(Project, slug=slug, deleted_at__isnull=True)
    project.update_status()
    project.update_raised_amount()

    # 計算達成率
    progress_percentage = calculate_progress_percentage(
        project.raised_amount, project.goal_amount
    )

    # 計算剩餘天數
    total_days = calculate_total_days(project.end_at)

    # 計算贊助人數
    backers_count = project.get_backers_count()

    # 檢查用戶是否已收藏和按讚
    collected = None
    favorited = None
    if request.user.is_authenticated:
        collected = CollectProject.objects.filter(
            account=request.user, project=project
        ).first()
        favorited = FavoritePrject.objects.filter(
            account=request.user, project=project
        ).first()

    # 獲取專案分類
    categories = Category.objects.filter(
        id__in=ProjectCategory.objects.filter(project_id=project.id).values_list(
            "category_id", flat=True
        )
    )

    parent_ids = [category.parent_id for category in categories if category.parent_id]
    parent_categories = Category.objects.filter(id__in=parent_ids)

    profile = project.account.profile
    comments = project.comments.filter(parent__isnull=True).order_by("-created_at")

    return render(
        request,
        "projects/public.html",
        {
            "project": project,
            "progress_percentage": progress_percentage,
            "total_days": total_days,
            "backers_count": backers_count,
            "collected": collected,
            "favorited": favorited,
            "categories": categories,
            "parent_categories": parent_categories,
            "profile": profile,
            "comments": comments,
            "user": request.user,
        },
    )


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


def projects_all(request):
    categories = Category.objects.filter(parent__isnull=True)
    projects = (
        Project.objects.prefetch_related("categories__parent")
        .filter(status="live", deleted_at__isnull=True)
        .order_by("-created_at")
    )

    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(
        request,
        "projects/projects_all.html",
        {"page_obj": page_obj, "categories": categories},
    )


@login_required
def gender_amount_scatter_excel(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)

    # 獲取每筆贊助的性別和金額
    sponsor_data = (
        Sponsor.objects.filter(project=project, reward__isnull=True)
        .select_related("account__profile")
        .values("account__profile__gender", "amount")
    )

    scatter_data = {"M": [], "F": [], "O": []}
    median_data = {"M": 0, "F": 0, "O": 0}

    # 整理贊助數據
    for entry in sponsor_data:
        gender = entry["account__profile__gender"]
        amount = entry["amount"]
        if gender in scatter_data:
            scatter_data[gender].append(float(amount))

    # 計算中位數
    for gender, amounts in scatter_data.items():
        if amounts:
            sorted_amounts = sorted(amounts)
            n = len(sorted_amounts)
            if n % 2 == 0:
                median_data[gender] = (
                    sorted_amounts[n // 2 - 1] + sorted_amounts[n // 2]
                ) / 2
            else:
                median_data[gender] = sorted_amounts[n // 2]

    # 建立 DataFrame
    data = []
    for gender, amounts in scatter_data.items():
        for amount in amounts:
            data.append(
                {
                    "性別": (
                        "男" if gender == "M" else "女" if gender == "F" else "其他"
                    ),
                    "金額": amount,
                }
            )
    for gender, median in median_data.items():
        data.append(
            {
                "性別": f"中位數 - {'男' if gender == 'M' else '女' if gender == 'F' else '其他'}",
                "金額": median,
            }
        )

    df = pd.DataFrame(data)

    # 將 DataFrame 輸出為 Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="gender_amount_scatter_{slug}.xlsx"'
    )
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="贊助數據")

    return response


@login_required
def gender_proportion_excel(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)

    # 使用 distinct() 確保只計算唯一贊助者
    gender_data = (
        Sponsor.objects.filter(project=project)
        .values("account__profile__gender")
        .distinct()
        .annotate(count=Count("account", distinct=True))
    )

    labels = []
    counts = []
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
        counts.append(count)
        total_count += count

    # 構建 DataFrame
    data = {"性別": labels, "人數": counts}
    df = pd.DataFrame(data)

    # 新增總人數行
    df.loc[len(df.index)] = ["總人數", total_count]

    # 將 DataFrame 輸出為 Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="gender_proportion_{slug}.xlsx"'
    )
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="性別比例")

    return response


@login_required
def reward_grouped_bar_chart_excel(request, slug):
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

    # 構建 DataFrame
    rows = []
    for reward, group_counts in grouped_data.items():
        for combination, count in group_counts.items():
            gender, age_group = combination.split("_")
            rows.append(
                {"回饋": reward, "性別": gender, "年齡區間": age_group, "人數": count}
            )

    df = pd.DataFrame(rows)

    # 將 DataFrame 輸出為 Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="reward_grouped_bar_chart_{slug}.xlsx"'
    )

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="回饋分析")

    return response


@login_required
def daily_sponsorship_amount_excel(request, slug):
    from .models import Sponsor

    project = get_object_or_404(Project, slug=slug)
    sponsors = Sponsor.objects.filter(project=project)

    if not sponsors.exists():
        # 如果無贊助數據，返回空 Excel
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="daily_sponsorship_amount_{slug}.xlsx"'
        )
        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            pd.DataFrame({"日期": [], "每日金額": [], "累積金額": []}).to_excel(
                writer, index=False, sheet_name="每日累積金額"
            )
        return response

    # 計算每日金額和累積金額
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

    # 構建 DataFrame
    df = pd.DataFrame(
        {
            "日期": [date.strftime("%Y-%m-%d") for date in date_range],
            "每日金額": [daily_totals.get(date, 0) for date in date_range],
            "累積金額": cumulative_amount,
        }
    )

    # 輸出 Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="daily_sponsorship_amount_{slug}.xlsx"'
    )
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="每日累積金額")

    return response


def search_projects(request):
    form = ProjectSearchForm(request.GET or None)  # 初始化表單
    projects = Project.objects.filter(status="live", deleted_at__isnull=True)

    if form.is_valid():
        query = form.cleaned_data.get("query", "")
        status = form.cleaned_data.get("status", "")
        location = form.cleaned_data.get("location", "")

        if query:
            projects = projects.filter(
                Q(title__icontains=query)
                | Q(subtitle__icontains=query)
                | Q(story__icontains=query)
                | Q(status__icontains=query)
                | Q(location__icontains=query)
                | Q(categories__title__icontains=query)
            ).distinct()

        if status:
            projects = projects.filter(status=status)

        if location:
            projects = projects.filter(location__icontains=location)

    projects = projects.order_by('id') 

    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(
        request,
        "projects/search_results.html",
        {"page_obj": page_obj, "query": query},
    )
