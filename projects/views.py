from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProjectFrom
from .models import Project, CollectProject, FavoritePrject
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from comments.models import Comment
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Sum
from django.utils.timezone import make_aware
import datetime





@login_required
def index(request):
    account = request.user
    if request.POST:
        form = ProjectFrom(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.account = account
            project.save()
            return redirect("projects:show", slug=project.slug)
        else:
            return HttpResponse("輸入錯誤")

    projects = Project.objects.filter(account=account)
    for project in projects:
        project.update_status()  # 更新專案的上下架狀態
    return render(
        request, "projects/index.html", {"projects": projects, "account": account}
    )


@login_required
def new(request):
    account = request.user
    return render(request, "projects/new.html", {"account": account})


@login_required
def show(request, slug):
    project = get_object_or_404(Project, slug=slug)
    account = get_object_or_404(User, id=request.user.id)
    comments = project.comments.filter(parent__isnull=True).order_by("-id")

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
            form = ProjectFrom(request.POST, instance=project)
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

    return render(
        request,
        "projects/show.html",
        {
            "project": project,
            "collected": collected,
            "account": account,
            "favorited": favorited,
            "comments": comments,
        },
    )


@login_required
def edit(request, slug):
    project = get_object_or_404(Project, slug=slug)

    format_time_start = localtime(project.start_at).strftime("%Y-%m-%dT%H:%M")
    format_time_end = localtime(project.end_at).strftime("%Y-%m-%dT%H:%M")
    return render(
        request,
        "projects/edit.html",
        {
            "project": project,
            "format_time_start": format_time_start,
            "format_time_end": format_time_end,
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

    return redirect("projects:show", slug=project.slug)


def chart_page(request,slug):
    project = get_object_or_404(Project, slug=slug)

    return render(request, "projects/chart_page.html", {"slug": slug})


@login_required
def gender_proportion(request, slug):
    from .models import Sponsor
    project = get_object_or_404(Project, slug=slug)

    # 獲取贊助者的性別數據並分組統計
    gender_data = (
        Sponsor.objects.filter(project=project)  
        .values("account__profile__gender")  
        .annotate(count=Count("id"))  
    )

    # 構建數據
    labels = []
    data = []
    total_count = 0  # 初始化總人數

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
        total_count += count  # 累加總人數

    # 返回的 JSON 數據
    response_data = {
        "labels": labels,
        "datasets": [
            {
                "label": f"贊助者性別比例（總人數: {total_count}）",  # 添加總人數
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

    # 檢查是否有贊助紀錄
    sponsors = Sponsor.objects.filter(project=project)
    if not sponsors.exists():
        return JsonResponse({
            "labels": [],
            "datasets": [{
                "label": "Cumulative Amount",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 2,
                "data": [],
            }]
        })

    # 獲取日期範圍
    start_date = sponsors.order_by("created_at").first().created_at.date()
    end_date = sponsors.order_by("-created_at").first().created_at.date()

    # 用字典記錄每天的實際贊助金額
    daily_totals = {}
    
    # 先計算每天的贊助總額
    for sponsor in sponsors:
        date = sponsor.created_at.date()
        if date not in daily_totals:
            daily_totals[date] = 0
        daily_totals[date] += sponsor.amount

    # 產生日期序列並計算累積金額
    date_range = []
    cumulative_amount = []
    cumulative_total = 0
    
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        # 取得當天的贊助金額（如果沒有則為0）並加入累積總額
        daily_amount = daily_totals.get(current_date, 0)
        cumulative_total += daily_amount
        cumulative_amount.append(cumulative_total)
        current_date += datetime.timedelta(days=1)

    data = {
        "labels": [date.strftime("%Y-%m-%d") for date in date_range],
        "datasets": [{
            "label": "每日累積金額",
            "backgroundColor": "rgba(75, 192, 192, 0.2)",
            "borderColor": "rgba(75, 192, 192, 1)",
            "borderWidth": 2,
            "data": cumulative_amount,
        }]
    }
    
    return JsonResponse(data)

@login_required
def gender_amount_boxplot(request, slug):
    from .models import Sponsor
    from django.db.models import Min, Max, Avg, Q
    from decimal import Decimal
    
    project = get_object_or_404(Project, slug=slug)

    # 過濾贊助數據並分性別進行統計
    gender_data = (
        Sponsor.objects.filter(project=project, reward__isnull=True)
        .select_related('account__profile')
        .values("account__profile__gender", "amount")
    )

    # 構建數據
    gender_amounts = {"M": [], "F": [], "O": []}

    for entry in gender_data:
        gender = entry["account__profile__gender"]
        amount = entry["amount"]
        if gender in gender_amounts:
            gender_amounts[gender].append(amount)

    # 計算每個性別的箱型圖數據
    boxplot_data = []
    for gender, amounts in gender_amounts.items():
        if amounts:  # 確保有數據才計算
            sorted_amounts = sorted(amounts)
            n = len(sorted_amounts)
            
            # 計算四分位數
            q1_idx = int(n * 0.25)
            q2_idx = int(n * 0.5)  # 中位數
            q3_idx = int(n * 0.75)
            
            q1 = sorted_amounts[q1_idx]
            median = sorted_amounts[q2_idx]
            q3 = sorted_amounts[q3_idx]
            
            # 計算四分位距 (使用 Decimal)
            iqr = q3 - q1
            
            # 計算上下限 (使用 Decimal)
            lower_bound = max(min(sorted_amounts), q1 - iqr * Decimal('1.5'))
            upper_bound = min(max(sorted_amounts), q3 + iqr * Decimal('1.5'))
            
            # 找出離群值
            outliers = [x for x in sorted_amounts if x < lower_bound or x > upper_bound]
            
            boxplot_data.append({
                'min': float(lower_bound),
                'q1': float(q1),
                'median': float(median),
                'q3': float(q3),
                'max': float(upper_bound),
                'outliers': [float(x) for x in outliers]
            })
        else:
            boxplot_data.append({
                'min': 0,
                'q1': 0,
                'median': 0,
                'q3': 0,
                'max': 0,
                'outliers': []
            })

    response_data = {
        "labels": ["男", "女", "其他"],
        "datasets": [{
            "label": "贊助金額分布",
            "data": boxplot_data,
            "backgroundColor": ["#F8AFAF", "#A8D3F0", "#FFE69B"],
            "borderColor": "#FFFFFF",
            "borderWidth": 2
        }]
    }

    return JsonResponse(response_data)
