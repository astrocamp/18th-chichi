from django.shortcuts import render

# Create your views here.


def homepages(request):
    return render(request, "homepages/homepages.html")
