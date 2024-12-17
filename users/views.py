from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import UserForm


def index(request):
    if request.POST:
        form = UserForm(
            request.POST,
            request.FILES,
        )
        form.save()
        return redirect("users:index")

    users = User.objects.all()
    return render(
        request,
        "users/index.html",
        {"users": users},
    )


def new(request):
    if request.POST:
        form = UserForm(request.POST, request.FILES)
        form.save()
        return redirect("users:index")
    return render(
        request,
        "users/new.html",
    )


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
