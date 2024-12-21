from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

# Create your views here.


def homepages(request):
    if isinstance(request.user, AnonymousUser):
        account = None
    else:
        account = get_object_or_404(User, id=request.user.id)
    return render(request, "homepages/homepages.html",{"account":account})
