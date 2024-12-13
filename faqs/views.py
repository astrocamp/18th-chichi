from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import FaqForm
from .models import Faq

def index(request):
    if request.POST:
        form = FaqForm(request.POST)
        form.save()
        messages.success(request, "新增成功")
        return redirect("faqs:index")
    
    faqs = Faq.objects.order_by("-id")
    return render(request, "faqs/index.html", {"faqs": faqs})

def new(request):
    form = FaqForm()
    return render(request, "faqs/new.html", {"form": form})

def show(request, id):
    faq = get_object_or_404(Faq, id=id)
    if request.POST:
        form = FaqForm(request.POST, instance=faq)
        form.save()
        messages.success(request, "更新成功")
        return redirect("faqs:index")
    
    return render(request, "faqs/show.html", {"faq": faq})

def edit(request, id):
    faq = get_object_or_404(Faq, id=id)
    form = FaqForm(instance=faq)    
    return render(request, "faqs/edit.html", {"faq": faq, "form": form})

def delete(request, id):
    faq = get_object_or_404(Faq, id=id)
    if request.POST:
        faq.delete()
        messages.success(request, "刪除成功")
        return redirect("faqs:index")

    return render(request, "faqs/delete.html", {"faq": faq})
