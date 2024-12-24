from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm
from accounts.views import User
from django.utils import timezone


def profiles_index(request, id):
    account = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, account=account)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            profile.update_at = timezone.now()
            profile.save()
            return redirect("accounts:profiles_index", id=account.id)

    return render(
        request, "profiles/index.html", {"account": account, "profile": profile}
    )


def profiles_new(request, id):
    account = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, account=account)
    form = ProfileForm(request.FILES, instance=profile)
    return render(
        request,
        "profiles/new.html",
        {"profile": profile, "form": form, "account": account},
    )


def profiles_edit(request, id):
    account = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, account=account)
    format_time = profile.birthday.strftime("%Y-%m-%d")
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
