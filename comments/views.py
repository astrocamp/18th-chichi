from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from projects.models import Project
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.http import HttpResponse
from django.views.decorators.http import require_POST


@login_required
def new(request, slug):
    project = get_object_or_404(Project, slug=slug)
    comments = project.comments.order_by("-id")

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            new_comment = Comment.objects.create(
                project=project, content=content, account=request.user
            )
            # 如果是 HTMX 請求，回傳部分模板
            if request.headers.get("HX-Request"):
                return render(
                    request,
                    "comments/comment_item.html",
                    {"comment": new_comment, "project": project},
                )
        else:
            if request.headers.get("HX-Request"):
                return HttpResponse("留言內容不能為空。", status=400)
    return HttpResponse("無效的請求。", status=400)


@login_required
def reply(request, slug, comment_slug):
    project = get_object_or_404(Project, slug=slug)
    parent_comment = get_object_or_404(Comment, slug=comment_slug, project=project)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            new_reply = Comment.objects.create(
                project=project,
                content=content,
                account=request.user,
                parent=parent_comment,
            )
            if request.headers.get("HX-Request"):
                return render(
                    request,
                    "comments/reply_item.html",
                    {"comment": new_reply, "project": project},
                )

        else:
            if request.headers.get("HX-Request"):
                return HttpResponse("回覆內容不能為空。", status=400)

    return HttpResponse("無效的請求。", status=400)


@login_required
@require_POST
def delete(request, slug, comment_slug):
    project = get_object_or_404(Project, slug=slug)
    comment = get_object_or_404(Comment, slug=comment_slug, project=project)

    if request.user == comment.account:
        comment.delete()
        return HttpResponse("")
    return redirect("projects:show", slug=project.slug)


@login_required
def reply_form(request, slug, comment_slug):
    project = get_object_or_404(Project, slug=slug)
    parent_comment = get_object_or_404(Comment, slug=comment_slug, project=project)
    return render(
        request,
        "comments/reply_form.html",
        {
            "parent_comment": parent_comment,
            "project": project,
        },
    )
