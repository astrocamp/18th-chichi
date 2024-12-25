from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import RewardForm
from .models import Reward
from projects.models import Project
from django.http import HttpResponse
from projects.models import Sponsor
from django.contrib.auth.models import User




@login_required
def index(request, slug):
    project = get_object_or_404(Project ,slug=slug)
    if request.POST:
        form = RewardForm(request.POST)
        if form.is_valid():
            reward = form.save(commit=False)
            reward.project = project
            reward.save()
            messages.success(request, "新增成功")
            return redirect("projects:rewards_index", slug=project.slug)
        else:
            return HttpResponse("輸入錯誤")

    
    rewards = Reward.objects.filter(project=project)
    return render(request, "rewards/index.html", {"rewards": rewards, "project":project})

def new(request,slug):
    form = RewardForm()
    project = get_object_or_404(Project ,slug=slug)
    return render(request, "rewards/new.html", {"form": form, "project":project})


@login_required
def show(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
    if request.POST:
        form = RewardForm(request.POST, instance=reward)
        form.save()
        reward.update_at = timezone.now()
        reward.save()
        messages.success(request, "更新成功")
        return redirect("rewards:show",id=reward.id)

    return render(request, "rewards/show.html", {"reward": reward})


@login_required
def edit(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
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
        return redirect("projects:show", id=project.id)

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
