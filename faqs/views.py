from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .forms import FaqForm
from .models import Faq
from projects.models import Project

def index(request, id):
    project = get_object_or_404(Project, id=id)
    if request.POST:
        form = FaqForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.project = project
            faq.save()
            messages.success(request, "新增成功")
            return redirect("projects:faq_index", id=id)
    
    faqs = Faq.objects.filter(project=project)
    return render(request, "faqs/index.html", {"faqs": faqs, "project": project}) 

def new(request, id):
    project = get_object_or_404(Project, id=id)
    form = FaqForm()
    return render(request, "faqs/new.html", {"form": form, "project": project})

def show(request, id):
    faq = get_object_or_404(Faq, id=id)
    project = get_object_or_404(Project, id=faq.project.id)
    if request.POST:
        form = FaqForm(request.POST, instance=faq)
        form.save()
        faq.update_at = timezone.now()
        faq.save()
        messages.success(request, "更新成功")
        return redirect("projects:faq_index" ,id=project.id)
    
    return render(request, "faqs/show.html", {"faq": faq,} )

def edit(request, id):
    faq = get_object_or_404(Faq, id=id)
    form = FaqForm(instance=faq)    
    return render(request, "faqs/edit.html", {"faq": faq, "form": form, })

def delete(request, id):
    faq = get_object_or_404(Faq, id=id)
    project = get_object_or_404(Project, id=faq.project.id)
    if request.POST:
        faq.delete()
        messages.success(request, "刪除成功")
        return redirect("projects:faq_index", id = project.id)

    return render(request, "faqs/delete.html", {"faq": faq,})
