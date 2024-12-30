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
    return render(request, "rewards/index.html", {"rewards": rewards, "project":project})


@login_required
def new(request,slug):
    project = get_object_or_404(Project ,slug=slug)
    products = RewardProduct.objects.all()
    options = OptionalAdd.objects.all()
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
        # 獲取所有商品數據
            products = [
                name for key, name in request.POST.items()
                if key.startswith('products[') and name.strip()
            ]
            
            # 批量新增商品
            RewardProduct.objects.bulk_create([RewardProduct(name=name) for name in products])
            
            # 返回成功訊息
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
                    OptionalAdd(name=option["name"], price=option["price"]) for option in options
                ])
                # 返回成功訊息
                messages.success(request, f"成功新增 {len(options)} 個選項")
            else:
                messages.error(request, "沒有有效的選項提交")
        
        # 返回成功訊息

    prodcut = RewardProduct.objects.all()
    option = OptionalAdd.objects.all()

    return render(request, "rewards/reward_items.html", {"project":project,"prodcut":prodcut,"option":option})




@login_required
def show(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
    project = reward.project
    if reward.project.account != request.user:
        messages.error(request, "您無權訪問該頁面")
        return redirect("homapages:homepages")

    if request.POST:
        form = RewardForm(request.POST, instance=reward)
        form.save()
        reward.update_at = timezone.now()
        reward.save()
        messages.success(request, "更新成功")
        return redirect("rewards:show",slug=reward.slug)

    return render(request, "rewards/show.html", {"reward": reward,"project":project})

@login_required
def edit(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
    if reward.project.account != request.user:
        messages.error(request, "您無權修改該頁面")
        return redirect("homapages:homepages")

    form = RewardForm(instance=reward)
    return render(request, "rewards/edit.html", {"reward": reward, "form": form})


def delete(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
    project = get_object_or_404(Project, slug=reward.project.slug)
    if request.POST:
        reward.delete()
        messages.success(request, "刪除成功")
        return redirect("projects:rewards_index", slug = project.slug)
    
    return render(request, "rewards/delete.html", {"reward": reward})



def sponsor(request,slug):
    project = get_object_or_404(Project, slug=slug)
    rewards = Reward.objects.filter(project=project)
    return render(request, "rewards/sponsor.html", {"project": project,"rewards":rewards})





@login_required
def free_sponsor(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.POST:
        amount = request.POST.get("amount")
        amount = int(amount)
        Sponsor.objects.create(
            account=request.user,
            project=project,
            reward=None, 
            amount=amount,
        )
        project.raised_amount = int(project.raised_amount or 0) + amount
        project.save()

        messages.success(request, f"感謝您贊助了 {amount} 元！")
        return redirect("projects:free_confirm", id=project.id)

    return render(request, "rewards/sponsor", {"project": project})    



@login_required
def reward_sponsor(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.POST:
        reward_slug = request.POST.get("reward")
        reward = get_object_or_404(Reward, slug=reward_slug)
        amount = int(reward.price)  
        Sponsor.objects.create(
            account=request.user,
            project=project,
            reward=reward,
            amount=amount,
        )
        project.raised_amount = int(project.raised_amount or 0) + amount
        project.save()

        messages.success(request, f"感謝您選擇了獎勵「{reward.title}」，贊助了 {amount} 元！")
        return redirect("projects:show", slug=project.slug)

    rewards = project.rewards.all()
    return render(request, "reward_sponsor_form.html", {"project": project, "rewards": rewards})


def free_confirm(request,slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "rewards/free_confirm.html", {"project": project})
