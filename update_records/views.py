from django.shortcuts import render, redirect, get_object_or_404
from .forms import UpdateRecordFrom
from .models import UpdateRecord
from projects.models import Project
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages


def index(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "請先登入")
            return redirect("projects:update_records_index", slug=project.slug)
        UpdateRecord.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            project=project,
        )
        return redirect("projects:update_records_index", slug=project.slug)

    update_records = UpdateRecord.objects.filter(
        project=project, deleted_at__isnull=True
    )

    # 如果是htmx請求，返回projects下的內容模板
    if request.headers.get("HX-Request"):
        return render(
            request,
            "projects/partials/update_records_content.html",
            {"update_records": update_records},
        )

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
        update_record.deleted_at = timezone.now()
        update_record.save()
        return redirect("projects:update_records_index", slug=project.slug)

    return render(
        request,
        "update_records/delete.html",
        {"update_record": update_record, "project": project},
    )
