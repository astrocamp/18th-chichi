from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from users.views import User as UserProfile
from django.contrib.auth.models import User

def index(request ,id):
    account = get_object_or_404(User, id=id)
    return render(request, "accounts/index.html",{"account":account})
    




def login(request):
    if request.POST:
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user is not None:
            login_user(request, user)
            messages.success(request, "登入成功")
            return redirect("homepages:homepages")
        else:
            messages.success(request, "登入失敗")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


def register(request):
    if request.POST:
        form = UserCreationForm(request.POST)        
        if form.is_valid():
            account = form.save()
            UserProfile.objects.create(
                name=account.username,
                account=account
            )
            messages.success(request, "註冊成功")
            return redirect("homepages:homepages")
        else:
            return HttpResponse(form.error_messages)

    return render(request, "accounts/register.html")


@require_POST
@login_required
def logout(request):
    logout_user(request)
    messages.success(request, "已登出")
    return redirect("homepages:homepages")
