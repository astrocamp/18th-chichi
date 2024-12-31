from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    account = request.user
    profile = get_object_or_404(Profile,account=account)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile:index")

    return render(request, "profiles/index.html", {"account":account, "profile":profile})

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
