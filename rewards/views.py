from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import RewardForm, ProductForm, OptionalAdd
from .models import Reward, RewardProduct, OptionalAdd
from projects.models import Project
from django.http import HttpResponse
from projects.models import Sponsor
from django.contrib.auth.models import User
from django.urls import reverse
from payments.ecpay_sdk import ECPayPayment
from payments.models import Order
from datetime import datetime


@login_required
def index(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if project.account != request.user:
        messages.error(request, "您無權訪問該頁面")
        return redirect("homapages:homepages")
    if request.method == "POST" and "reward" in request.POST:
        reward_form = RewardForm(request.POST)
        if reward_form.is_valid():
            reward = reward_form.save(commit=False)
            reward.project = project
            reward.save()

            product_ids = request.POST.getlist("products")
            if product_ids:
                products = RewardProduct.objects.filter(id__in=product_ids)
                for product in products:
                    product.rewards.add(reward)

            option_ids = request.POST.getlist("options")
            if option_ids:
                options = OptionalAdd.objects.filter(id__in=option_ids)
                for option in options:
                    option.rewards.add(reward)

            messages.success(request, "Reward 新增成功")
            return redirect("projects:rewards_index", slug=project.slug)
        else:
            messages.error(request, "Reward 表單有誤，請檢查後再提交")
    rewards = Reward.objects.filter(project_id=project.id)
    products = RewardProduct.objects.filter(
        project_id=project.id,
    )
    options = OptionalAdd.objects.filter(project_id=project.id)

    return render(
        request,
        "rewards/index.html",
        {
            "rewards": rewards,
            "project": project,
            "products": products,
            "options": options,
        },
    )


@login_required
def new(request, slug):
    project = get_object_or_404(Project, slug=slug)
    products = RewardProduct.objects.filter(project_id=project.id)
    options = OptionalAdd.objects.filter(project_id=project.id)
    if project.account != request.user:
        messages.error(request, "您無權新增該頁面")
        return redirect("homapages:homepages")

    form = RewardForm()
    return render(
        request,
        "rewards/new.html",
        {"form": form, "project": project, "products": products, "options": options},
    )


@login_required
def reward_items(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if project.account != request.user:
        messages.error(request, "您無權新增該頁面")
        return redirect("homapages:homepages")
    if request.POST:
        if "save_products" in request.POST:
            products = [
                name
                for key, name in request.POST.items()
                if key.startswith("products[") and name.strip()
            ]

            RewardProduct.objects.bulk_create(
                [RewardProduct(name=name, project_id=project.id) for name in products]
            )
            messages.success(request, f"成功新增 {len(products)} 個商品")

        if "save_options" in request.POST:
            options = []

            for key, name in request.POST.items():
                if (
                    key.startswith("options[")
                    and key.endswith("][name]")
                    and name.strip()
                ):
                    index = key.split("[")[1].split("]")[0]
                    price = request.POST.get(f"options[{index}][price]", "").strip()
                    if price:
                        options.append({"name": name, "price": price})

            if options:
                OptionalAdd.objects.bulk_create(
                    [
                        OptionalAdd(
                            name=option["name"],
                            price=option["price"],
                            project_id=project.id,
                        )
                        for option in options
                    ]
                )
                messages.success(request, f"成功新增 {len(options)} 個選項")
            else:
                messages.error(request, "沒有有效的選項提交")
    products = RewardProduct.objects.filter(
        project_id=project.id,
    )
    options = OptionalAdd.objects.filter(project_id=project.id)

    return render(
        request,
        "rewards/reward_items.html",
        {"project": project, "products": products, "options": options},
    )


@login_required
def show(request, id):
    reward = get_object_or_404(Reward, id=id)
    project = reward.project
    if reward.project.account != request.user:
        messages.error(request, "您無權訪問該頁面")
        return redirect("homapages:homepages")

    if request.method == "POST":
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            reward = form.save(commit=False)
            reward.save()

            reward.rewardproduct_set.clear()
            product_ids = request.POST.getlist("products")
            if product_ids:
                products = RewardProduct.objects.filter(
                    id__in=product_ids,
                )
                reward.rewardproduct_set.add(*products)

            reward.optionaladd_set.clear()
            option_ids = request.POST.getlist("options")
            if option_ids:
                options = OptionalAdd.objects.filter(
                    id__in=option_ids,
                )
                reward.optionaladd_set.add(*options)

            messages.success(request, "Reward 更新成功")
            return redirect("rewards:show", id=reward.id)
        else:
            messages.error(request, "表單提交有誤，請檢查輸入內容")

    form = RewardForm(instance=reward)

    return render(request, "rewards/show.html", {"reward": reward, "project": project})


@login_required
def edit(request, id):
    reward = get_object_or_404(Reward, id=id)
    project = reward.project
    if reward.project.account != request.user:
        messages.error(request, "您無權修改該頁面")
        return redirect("homapages:homepages")

    form = RewardForm(instance=reward)
    products = RewardProduct.objects.filter(project=project)
    options = OptionalAdd.objects.filter(project=project)
    related_products = RewardProduct.objects.filter(
        rewards=reward,
    )
    related_options = OptionalAdd.objects.filter(
        rewards=reward,
    )
    return render(
        request,
        "rewards/edit.html",
        {
            "reward": reward,
            "form": form,
            "products": products,
            "options": options,
            "related_products": related_products,
            "related_options": related_options,
        },
    )


@login_required
def sponsor(request, slug):
    project = get_object_or_404(Project, slug=slug)
    rewards = Reward.objects.filter(project_id=project.id)

    reward_details = []
    for reward in rewards:
        products = RewardProduct.objects.filter(rewards=reward)
        options = OptionalAdd.objects.filter(rewards=reward)
        reward_details.append(
            {
                "reward": reward,
                "products": products,
                "options": options,
            }
        )

    return render(
        request,
        "rewards/sponsor.html",
        {
            "project": project,
            "reward_details": reward_details,
        },
    )


@login_required
def free_sponsor(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.POST:
        amount = request.POST.get("amount")
        Sponsor.objects.create(
            account=request.user,
            project_id=project.id,
            reward=None,
            amount=amount,
            status="pending",
        )
        return redirect(
            f"{reverse('projects:free_sponsor_confirm', kwargs={'slug': project.slug})}?amount={amount}"
        )
    return render(request, "rewards/sponsor", {"project": project})


@login_required
def reward_sponsor(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == "POST":
        reward_id = request.POST.get("reward")
        reward = get_object_or_404(Reward, id=reward_id, project=project)

        # 創建 Sponsor 記錄
        amount = reward.price if reward.price is not None else 0
        sponsor = Sponsor.objects.create(
            account=request.user,
            project=project,
            reward=reward,
            amount=amount,
            status="pending",
        )

        # 重定向到選擇配件頁面
        return redirect("projects:reward_sponsor_options", slug=project.slug)

    # 如果不是 POST 請求，重定向回專案頁面
    return redirect("projects:public", slug=project.slug)


@login_required
def reward_sponsor_options(request, slug):
    project = get_object_or_404(Project, slug=slug)
    sponsors = Sponsor.objects.filter(account=request.user, project=project)
    sponsor = sponsors.order_by("-id").first()

    if not sponsor or not sponsor.reward:
        messages.error(request, "找不到相關的回饋項目")
        return redirect("projects:sponsor", slug=project.slug)

    reward = sponsor.reward
    reward_products = RewardProduct.objects.filter(
        project=project, rewards=reward
    )
    optional_adds = OptionalAdd.objects.filter(
        project=project, rewards=reward,
    )

    if request.POST:
        if "delete_sponsor" in request.POST:
            sponsor.delete()
            return redirect("projects:sponsor", slug=project.slug)

        amount = int(request.POST.get("amount", reward.price))
        additional_product_ids = request.POST.getlist("additional_products")

        additional_amount = 0
        additional_products = []
        if additional_product_ids:
            additional_products = OptionalAdd.objects.filter(
                id__in=additional_product_ids
            )
            additional_amount = sum(
                int(product.price) for product in additional_products
            )

        sponsor.amount = amount + additional_amount
        sponsor.save()

        request.session["sponsor_data"] = {
            "amount": int(amount),
            "additional_amount": int(additional_amount),
            "additional_product_ids": [str(id) for id in additional_product_ids],
        }

        return redirect("projects:reward_sponsor_confirm", slug=project.slug)

    return render(
        request,
        "rewards/reward_sponsor_options.html",
        {
            "project": project,
            "reward": reward,
            "reward_products": reward_products,
            "optional_adds": optional_adds,
            "amount": int(sponsor.amount),
        },
    )


@login_required
def reward_sponsor_confirm(request, slug):
    project = get_object_or_404(Project, slug=slug)
    sponsors = Sponsor.objects.filter(account=request.user, project=project)
    sponsor = sponsors.order_by("-id").first()

    if not sponsor or not sponsor.reward:
        messages.error(request, "找不到相關的回饋項目")
        return redirect("projects:sponsor", slug=project.slug)

    sponsor_data = request.session.get("sponsor_data", {})
    amount = int(sponsor_data.get("amount", int(sponsor.reward.price)))
    additional_amount = int(sponsor_data.get("additional_amount", 0))
    additional_product_ids = sponsor_data.get("additional_product_ids", [])

    additional_products = []
    if additional_product_ids:
        additional_products = OptionalAdd.objects.filter(id__in=additional_product_ids)

    total_amount = amount + additional_amount

    if request.POST:
        if "delete_sponsor" in request.POST:
            sponsor.delete()
            return redirect("projects:sponsor", slug=project.slug)

        order_id = f"RS{datetime.now().strftime('%Y%m%d%H%M%S')}"
        description = f"{project.title} - {sponsor.reward.title}"
        if additional_products:
            description += " (含加購商品)"

        # 建立訂單時加入 user 和 reward
        order = Order.objects.create(
            order_id=order_id,
            amount=total_amount,
            description=description,
            user=request.user,
            reward=sponsor.reward,
            quantity=1,  # 預設數量為 1
        )

        ecpay = ECPayPayment()
        order_params = ecpay.create_order(
            order_id=order_id, amount=total_amount, description=description
        )

        if "sponsor_data" in request.session:
            del request.session["sponsor_data"]

        return render(
            request,
            "payments/checkout.html",
            {"payment_url": ecpay.payment_url, "order_params": order_params},
        )

    return render(
        request,
        "rewards/reward_sponsor_confirm.html",
        {
            "project": project,
            "sponsor": sponsor,
            "reward": sponsor.reward,
            "reward_products": RewardProduct.objects.filter(
                project=project, rewards=sponsor.reward
            ),
            "additional_products": additional_products,
            "amount": amount,
            "additional_amount": additional_amount,
            "total_amount": total_amount,
        },
    )


def free_sponsor_confirm(request, slug):
    project = get_object_or_404(Project, slug=slug)
    sponsors = Sponsor.objects.filter(account=request.user, project=project)
    sponsor = sponsors.order_by("-id").first()
    amount = request.GET.get("amount", sponsor.amount if sponsor else 0)

    if request.POST:
        if "delete_sponsor" in request.POST:
            sponsor.delete()
            return redirect("projects:sponsor", slug=project.slug)
        else:
            order_id = f"FS{datetime.now().strftime('%Y%m%d%H%M%S')}"
            description = f"{project.title} - 自由贊助"

            # 建立訂單時加入 user，reward 設為 null=True
            order = Order.objects.create(
                order_id=order_id,
                amount=amount,
                description=description,
                user=request.user,
                reward=None,  # 自由贊助沒有回饋項目
                quantity=1,
            )

            ecpay = ECPayPayment()
            order_params = ecpay.create_order(
                order_id=order_id, amount=amount, description=description
            )

            return render(
                request,
                "payments/checkout.html",
                {"payment_url": ecpay.payment_url, "order_params": order_params},
            )

    return render(
        request,
        "rewards/free_sponsor_confirm.html",
        {"project": project, "sponsor": sponsor, "amount": amount},
    )


def rewards_content(request, slug):
    """處理贊助方案內容的視圖函數"""
    from projects.models import Project  # 在函數內部導入以避免循環引用

    project = get_object_or_404(Project, slug=slug)
    rewards = Reward.objects.filter(project=project).order_by("price")

    return render(
        request,
        "rewards/partials/rewards_content.html",
        {
            "project": project,
            "rewards": rewards,
        },
    )
