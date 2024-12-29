from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from projects.models import Project
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def index(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        comment = Comment()
        comment.content = request.POST.get("content")
        comment.project = project
        comment.account = request.user
        comment.save()

        return redirect("projects:comment_index", slug=project.slug)

    comments = Comment.objects.filter(project=project)

    return render(
        request, "comments/index.html", {"comments": comments, "project": project}
    )


@login_required
def new(request, slug):
    project = get_object_or_404(Project, slug=slug)

    return render(request, "comments/new.html", {"project": project})


@login_required
def show(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    project = comment.project
    if request.POST:
        comment.content = request.POST.get("content")
        comment.update_at = timezone.now()
        comment.save()
        return redirect("comments:show", slug=comment.slug)
    return render(
        request, "comments/show.html", {"comment": comment, "project": project}
    )


@login_required
def edit(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    project = comment.project
    return render(
        request, "comments/edit.html", {"comment": comment, "project": project}
    )


@login_required
def delete(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    project = comment.project
    if request.POST:
        comment.delete()
        return redirect("projects:comment_index", slug=project.slug)
    return render(
        request, "comments/delete.html", {"comment": comment, "project": project}
    )
