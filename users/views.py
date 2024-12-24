from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm
from accounts.views import User
from django.utils import timezone



def profiles_index(request,id):
    account = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile,account=account)
    if request.POST:
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            profile.update_at = timezone.now()
            profile.save()
            return redirect("accounts:profiles_index", id =account.id)

    return render(request, "profiles/index.html", {"account":account, "profile":profile})




def profiles_new(request, id):
    account = get_object_or_404(User , id=id)
    profile = get_object_or_404(Profile, account=account)
    form = ProfileForm(request.FILES, instance=profile)
    return render(
        request,
        "profiles/new.html",
        {"profile": profile,  "form": form, "account":account},
    )


<<<<<<< HEAD
def profiles_edit(request, id):
    account = get_object_or_404(User , id=id)
    profile = get_object_or_404(Profile, account=account)
    format_time = profile.birthday.strftime("%Y-%m-%d")
    form = ProfileForm(request.FILES, instance=profile)
=======
def new(request):
    if request.POST:
        form = UserForm(request.POST, request.FILES)
        form.save()
        return redirect("users:index")
>>>>>>> 589bbb8 (feat:upload function)
    return render(
        request,
        "profiles/edit.html",
        {"profile": profile,  "form": form, "account":account,"format_time":format_time},
    )

<<<<<<< HEAD
=======

def show(request, id):
    user = get_object_or_404(User, id=id)
    if request.POST:
        form = UserForm(request.POST, request.FILES, instance=user)
        form.save()
        return redirect("users:index")

    return render(
        request,
        "users/show.html",
        {"user": user},
    )


def edit(request, id):
    user = get_object_or_404(User, id=id)
    format_time = user.birthday.strftime("%Y-%m-%d")
    form = UserForm(request.FILES, instance=user)
    return render(
        request,
        "users/edit.html",
        {"user": user, "format_time": format_time, "form": form},
    )


def delete(request, id):
    user = get_object_or_404(User, id=id)
    if request.POST:
        user.delete()
        return redirect("users:index")
    return render(
        request,
        "users/delete.html",
        {"user": user},
    )
>>>>>>> 589bbb8 (feat:upload function)
