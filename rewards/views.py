from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .forms import RewardForm
from .models import Reward

def index(request):
    if request.POST:
        form = RewardForm(request.POST)
        form.save()
        messages.success(request, "新增成功")
        return redirect("rewards:index")
    
    rewards = Reward.objects.order_by("-id")
    return render(request, "rewards/index.html", {"rewards": rewards})

def new(request):
    form = RewardForm()
    return render(request, "rewards/new.html", {"form": form})

def show(request, id):
    reward = get_object_or_404(Reward, id=id)
    if request.POST:
        form = RewardForm(request.POST, instance=reward)
        form.save()
        reward.update_at = timezone.now()
        reward.save()
        messages.success(request, "更新成功")
        return redirect("rewards:index")

    return render(request, "rewards/show.html", {"reward": reward})

def edit(request, id):
    reward = get_object_or_404(Reward, id=id)
    form = RewardForm(instance=reward)
    return render(request, "rewards/edit.html", {"reward": reward, "form": form})

def delete(request, id):
    reward = get_object_or_404(Reward, id=id)
    if request.POST:
        reward.delete()
        messages.success(request, "刪除成功")
        return redirect("rewards:index")
    
    return render(request, "rewards/delete.html", {"reward": reward})