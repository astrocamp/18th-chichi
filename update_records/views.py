from django.shortcuts import render, redirect, get_object_or_404
from .forms import UpdateRecordFrom
from .models import UpdateRecord
from projects.models import Project
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def index(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == "POST":
        UpdateRecord.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            project=project,
        )
        return redirect("projects:update_records_index", slug=project.slug)

    update_records = UpdateRecord.objects.filter(project=project)
    return render(
        request,
        "update_records/index.html",
        {"update_records": update_records, "project": project},
    )


@login_required
def new(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "update_records/new.html", {"project": project})


@login_required
def show(request, slug):
    update_record = get_object_or_404(UpdateRecord, slug=slug)
    project = update_record.project

    if request.POST:
        form = UpdateRecordFrom(request.POST, instance=update_record)
        form.save()
        update_record.update_at = timezone.now()
        update_record.save()
        return redirect("update_records:show", slug=update_record.slug)

    return render(
        request,
        "update_records/show.html",
        {"update_record": update_record, "project": project},
    )


@login_required
def edit(request, slug):
    update_record = get_object_or_404(UpdateRecord, slug=slug)
    project = update_record.project

    return render(
        request,
        "update_records/edit.html",
        {"update_record": update_record, "project": project},
    )


@login_required
def delete(request, slug):
    update_record = get_object_or_404(UpdateRecord, slug=slug)
    project = update_record.project

    if request.POST:
        update_record.delete()
        return redirect("projects:update_records_index", slug=project.slug)

    return render(
        request,
        "update_records/delete.html",
        {"update_record": update_record, "project": project},
    )
