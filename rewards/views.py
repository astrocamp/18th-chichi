from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import RewardForm,ProductForm,OptionalAdd
from .models import Reward ,RewardProduct,OptionalAdd
from projects.models import Project
from django.http import HttpResponse
from projects.models import Sponsor
from django.contrib.auth.models import User
from django.urls import reverse


@login_required
def index(request, slug):
    project = get_object_or_404(Project ,slug=slug)
    if project.account != request.user:
        messages.error(request, "您無權訪問該頁面")
        return redirect("homapages:homepages")
    if request.method == "POST" and "reward" in request.POST:
        # 保存 Reward
        reward_form = RewardForm(request.POST)
        if reward_form.is_valid():
            reward = reward_form.save(commit=False)
            reward.project = project
            reward.save()

            # 保存與 Reward 關聯的產品
            product_ids = request.POST.getlist('products')  # 接收多選框選擇的產品 ID
            if product_ids:
                products = RewardProduct.objects.filter(id__in=product_ids)
                for product in products:
                    product.rewards.add(reward)  # 添加 Reward 與產品的多對多關聯

            # 保存與 Reward 關聯的附加選項
            option_ids = request.POST.getlist('options')  # 接收多選框選擇的附加選項 ID
            if option_ids:
                options = OptionalAdd.objects.filter(id__in=option_ids)
                for option in options:
                    option.rewards.add(reward)  # 添加 Reward 與附加選項的多對多關聯

            # 返回成功訊息並重定向
            messages.success(request, "Reward 新增成功")
            return redirect("projects:rewards_index", slug=project.slug)
        else:
            # 如果 Reward 表單驗證失敗
            messages.error(request, "Reward 表單有誤，請檢查後再提交")


    
    rewards = Reward.objects.filter(project=project)
    products = RewardProduct.objects.filter(project=project)
    options = OptionalAdd.objects.filter(project=project)

    return render(request, "rewards/index.html", {"rewards": rewards, "project":project,"products":products,"options":options})


@login_required
def new(request,slug):
    project = get_object_or_404(Project ,slug=slug)
    products = RewardProduct.objects.filter(project=project)
    options = OptionalAdd.objects.filter(project=project)
    if project.account != request.user:
        messages.error(request, "您無權新增該頁面")
        return redirect("homapages:homepages")

    form = RewardForm()
    return render(request, "rewards/new.html", {"form": form, "project":project,"products":products,"options":options})


@login_required
def reward_items(request,slug):
    project = get_object_or_404(Project ,slug=slug)
    if project.account != request.user:
        messages.error(request, "您無權新增該頁面")
        return redirect("homapages:homepages")
    if request.POST: 
        if "save_products" in request.POST:
            products = [
                name for key, name in request.POST.items()
                if key.startswith('products[') and name.strip()
            ]
            
            RewardProduct.objects.bulk_create([RewardProduct(name=name,project=project) for name in products])          
            messages.success(request, f"成功新增 {len(products)} 個商品")

        if "save_options" in request.POST:
            options = []
    
    # 獲取所有選項數據
            for key, name in request.POST.items():
                if key.startswith('options[') and key.endswith('][name]') and name.strip():
                    index = key.split('[')[1].split(']')[0]  # 提取索引值
                    price = request.POST.get(f"options[{index}][price]", "").strip()
                    if price:  # 確保價格存在
                        options.append({"name": name, "price": price})
        
    # 批量新增選項
            if options:  # 確保有選項
                OptionalAdd.objects.bulk_create([
                    OptionalAdd(name=option["name"], price=option["price"],project=project) for option in options
                ])
                messages.success(request, f"成功新增 {len(options)} 個選項")
            else:
                messages.error(request, "沒有有效的選項提交")
        

    products = RewardProduct.objects.filter(project=project)
    options = OptionalAdd.objects.filter(project=project)

    return render(request, "rewards/reward_items.html", {"project":project,"products":products,"options":options})




@login_required
def show(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
    project = reward.project
    if reward.project.account != request.user:
        messages.error(request, "您無權訪問該頁面")
        return redirect("homapages:homepages")
    

    if request.method == "POST":
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            reward = form.save(commit=False)
            reward.save()

            # 更新與 Reward 關聯的商品
            reward.rewardproduct_set.clear()  # 清空之前的關聯
            product_ids = request.POST.getlist('products')
            if product_ids:
                products = RewardProduct.objects.filter(id__in=product_ids)
                reward.rewardproduct_set.add(*products)  # 使用 add 批量添加新關聯

            # 更新與 Reward 關聯的附加選項
            reward.optionaladd_set.clear()  # 清空之前的關聯
            option_ids = request.POST.getlist('options')
            if option_ids:
                options = OptionalAdd.objects.filter(id__in=option_ids)
                reward.optionaladd_set.add(*options)  # 使用 add 批量添加新關聯

            messages.success(request, "Reward 更新成功")
            return redirect("rewards:show", id=reward.slug)
        else:
            messages.error(request, "表單提交有誤，請檢查輸入內容")

    form = RewardForm(instance=reward)

    return render(request, "rewards/show.html", {"reward": reward,"project":project})

@login_required
def edit(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
    project = reward.project
    if reward.project.account != request.user:
        messages.error(request, "您無權修改該頁面")
        return redirect("homapages:homepages")

    form = RewardForm(instance=reward)
    products = RewardProduct.objects.filter(project=project)
    options = OptionalAdd.objects.filter(project=project)
    related_products = RewardProduct.objects.filter(rewards=reward)
    related_options = OptionalAdd.objects.filter(rewards=reward)
    return render(request, "rewards/edit.html", {"reward": reward, "form": form,"products":products,"options":options,"related_products":related_products,"related_options":related_options})


def delete(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
    project = get_object_or_404(Project, slug=reward.project.slug)
    if request.POST:
        reward.delete()
        messages.success(request, "刪除成功")
        return redirect("projects:rewards_index", slug = project.slug)
    
    return render(request, "rewards/delete.html", {"reward": reward})




@login_required
def sponsor(request, slug):
    project = get_object_or_404(Project, slug=slug)
    rewards = Reward.objects.filter(project=project)

    reward_details = []
    for reward in rewards:
        products = RewardProduct.objects.filter(rewards=reward)
        options = OptionalAdd.objects.filter(rewards=reward)
        reward_details.append({
            "reward": reward,
            "products": products,
            "options": options,
        })

    return render(request, "rewards/sponsor.html", {
        "project": project,
        "reward_details": reward_details,
    })




@login_required
def free_sponsor(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.POST:
        amount = request.POST.get("amount")
        Sponsor.objects.create(
            account=request.user,
            project=project,
            reward=None, 
            amount=amount,
            status='pending',
        )
        # project.raised_amount = int(project.raised_amount or 0) + amount
        # project.save()

        # messages.success(request, f"感謝您贊助了 {amount} 元！")
        return redirect(f"{reverse('projects:free_confirm', kwargs={'id': project.id})}?amount={amount}")
    return render(request, "rewards/sponsor", {"project": project})    



@login_required
def reward_sponsor(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.POST:
        reward_slug = request.POST.get("reward")
        reward = get_object_or_404(Reward, slug=reward_slug)
        # price = reward.price if reward.price is not None else 0
        amount = reward.price if reward.price is not None else 0
        Sponsor.objects.create(
            account=request.user,
            project=project,
            reward=reward,
            amount=amount,
        )
        # project.raised_amount = int(project.raised_amount or 0) + amount
        # project.save()

        # messages.success(request, f"感謝您選擇了獎勵「{reward.title}」，贊助了 {amount} 元！")
        return redirect(f"{reverse('projects:free_confirm', kwargs={'slug': project.slug})}?amount={amount}")

    rewards = project.rewards.all()
    return render(request, "reward_sponsor_form.html", {"project": project, "rewards": rewards})

def free_confirm(request,slug):
    project = get_object_or_404(Project, slug=slug)
    reward = get_object_or_404(Reward, project=project)
    sponsors = Sponsor.objects.filter(account=request.user, project=project)
    sponsor = sponsors.order_by('-id').first()
    amount = request.GET.get('amount', sponsor.amount) 
    is_reward_sponsor = sponsor.reward is not None
    optional_adds = OptionalAdd.objects.filter(project=project, rewards=reward)
    reward_products = RewardProduct.objects.filter(project=project, rewards=reward)

    if request.POST:
        if "delete_sponsor" in request.POST:
            sponsor.delete()   
            return redirect("projects:sponsor", slug=project.slug)


    return render(request, "rewards/confirm.html", {"project": project,"sopnsor":sponsor,"amount":amount,"is_reward_sponsor": is_reward_sponsor,
            "reward": sponsor.reward if is_reward_sponsor else None,"optional_adds":optional_adds,"reward_products":reward_products})
