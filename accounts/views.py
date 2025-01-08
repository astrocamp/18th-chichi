from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django import forms
from projects.models import Sponsor
from users.models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密碼不匹配")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


@login_required
def index(request):
    account = request.user
    # 獲取用戶的 profile
    try:
        profile = Profile.objects.get(account=account)
    except Profile.DoesNotExist:
        # 如果找不到 profile，創建一個新的
        profile = Profile.objects.create(
            account=account,
            name=account.username,
            location="",
            bio="",
            birthday=None,
            website="",
        )

    # 獲取用戶贊助的專案，包含贈品資訊
    sponsored_projects = (
        Sponsor.objects.filter(account=account, status="paid")
        .select_related("project", "reward")
        .order_by("-created_at")
    )

    return render(
        request,
        "accounts/index.html",
        {
            "user": account,
            "profile": profile,
            "sponsored_projects": sponsored_projects,
        },
    )


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
            messages.error(request, "登入失敗")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


def register(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            account = form.save()
            Profile.objects.get_or_create(
                name=account.username,
                account=account,
                location="",
                bio="",
                birthday=None,
                website="",
            )
            messages.success(request, "註冊成功")
            return redirect("homepages:homepages")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, "accounts/register.html")

    return render(request, "accounts/register.html")


@require_POST
@login_required
def logout(request):
    logout_user(request)
    messages.success(request, "已登出")
    return redirect("homepages:homepages")
