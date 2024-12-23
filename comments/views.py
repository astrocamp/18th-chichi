from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from projects.models import Project
from django.utils import timezone
from projects.models import Project


def index(request, id):
    project = get_object_or_404(Project, id=id)
    if request.POST:
        comment = Comment()
        comment.content = request.POST.get("content")
        comment.project = project
        comment.save()

        return redirect("projects:comment_index", id=project.id)

    comments = Comment.objects.filter(project=project)

    return render(
        request, "comments/index.html", {"comments": comments, "project": project}
    )


def new(request, id):
    project = get_object_or_404(Project, id=id)

    return render(request, "comments/new.html", {"project": project})


def show(request, id):
    comment = get_object_or_404(Comment, id=id)
    project = get_object_or_404(Project, id=comment.project.id)
    if request.POST:
        comment.content = request.POST.get("content")
        comment.update_at = timezone.now()
        comment.save()
        return redirect("comments:show", id=comment.id)
    return render(
        request, "comments/show.html", {"comment": comment, "project": project}
    )


def edit(request, id):
    comment = get_object_or_404(Comment, id=id)
    return render(request, "comments/edit.html", {"comment": comment})


def delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    project = get_object_or_404(Project, id=comment.project.id)
    if request.POST:
        comment.delete()
        return redirect("projects:comment_index" , id=project.id)
    return render(request, "comments/delete.html", {"comment": comment})
