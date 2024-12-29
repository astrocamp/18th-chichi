from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import FaqForm
from .models import Faq
from projects.models import Project


@login_required
def index(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        form = FaqForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.project = project
            faq.save()
            messages.success(request, "新增成功")
            return redirect("projects:faq_index", slug=project.slug)

    faqs = Faq.objects.filter(project=project)
    return render(request, "faqs/index.html", {"faqs": faqs, "project": project})


@login_required
def new(request, slug):
    project = get_object_or_404(Project, slug=slug)
    form = FaqForm()
    return render(request, "faqs/new.html", {"form": form, "project": project})


@login_required
def show(request, slug):
    faq = get_object_or_404(Faq, slug=slug)
    project = faq.project
    if request.POST:
        form = FaqForm(request.POST, instance=faq)
        form.save()
        faq.update_at = timezone.now()
        faq.save()
        messages.success(request, "更新成功")
        return redirect("projects:faq_index", slug=project.slug)

    return render(
        request,
        "faqs/show.html",
        {
            "faq": faq,
            "project": project,
        },
    )


@login_required
def edit(request, slug):
    faq = get_object_or_404(Faq, slug=slug)
    project = faq.project
    form = FaqForm(instance=faq)
    return render(
        request,
        "faqs/edit.html",
        {
            "faq": faq,
            "form": form,
            "project": project,
        },
    )


@login_required
def delete(request, slug):
    faq = get_object_or_404(Faq, slug=slug)
    project = faq.project
    if request.POST:
        faq.delete()
        messages.success(request, "刪除成功")
        return redirect("projects:faq_index", slug=project.slug)

    return render(
        request,
        "faqs/delete.html",
        {
            "faq": faq,
            "project": project,
        },
    )
