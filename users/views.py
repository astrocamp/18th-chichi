from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required





@login_required
def new(request):
    account = request.user
    profile = get_object_or_404(Profile, account=account)
    form = ProfileForm(request.FILES, instance=profile)
    today = timezone.now().date()
    return render(
        request,
        "profiles/new.html",
        {"profile": profile, "form": form, "account": account, "today": today},
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
