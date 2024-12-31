from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    account = request.user
    profile = get_object_or_404(Profile, account=account)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "個人資料更新成功。")
            profile.updated_at = timezone.now()
            profile.save()
            return redirect("profile:index")
        else:
            messages.error(request, "個人資料新增失敗。")
            return render(
                request,
                "profiles/new.html",
                {"profile": profile, "form": form, "account": account},
            )

    return render(
        request, "profiles/index.html", {"account": account, "profile": profile}
    )


@login_required
def new(request):
    account = request.user
    profile = get_object_or_404(Profile, account=account)
    form = ProfileForm(request.FILES, instance=profile)
    return render(
        request,
        "profiles/new.html",
        {"profile": profile, "form": form, "account": account},
    )


@login_required
def edit(request):
    account = request.user
    profile = get_object_or_404(Profile, account=account)
    if profile.birthday:
        format_time = profile.birthday.strftime("%Y-%m-%d")
    else:
        format_time = ""

    form = ProfileForm(request.FILES, instance=profile)

    return render(
        request,
        "profiles/edit.html",
        {
            "profile": profile,
            "form": form,
            "account": account,
            "format_time": format_time,
        },
    )
