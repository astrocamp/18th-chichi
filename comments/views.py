from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from projects.models import Project
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages


def index(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        if not request.user.is_authenticated:
            messages.error(request, "請先登入")
            return redirect("projects:comment_index", slug=project.slug)
        comment = Comment()
        comment.content = request.POST.get("content")
        comment.project = project
        comment.account = request.user
        comment.save()
        return redirect("projects:comment_index", slug=project.slug)

    comments = (
        Comment.objects.filter(parent__isnull=True, project=project)
        .order_by("-created_at")
        .select_related("account", "project")
    )

    # 如果是htmx請求，返回projects下的內容模板
    if request.headers.get("HX-Request"):
        return render(
            request,
            "projects/partials/comments_content.html",
            {
                "comments": comments,
                "project": project,
                "user": request.user,
            },
        )

    return render(
        request,
        "comments/index.html",
        {
            "comments": comments,
            "project": project,
            "user": request.user,
        },
    )


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
        comment.save()
        return HttpResponse("")
    return redirect("projects:show", slug=project.slug)


@login_required
def reply_form(request, slug, comment_slug):
    project = get_object_or_404(Project, slug=slug)
    parent_comment = get_object_or_404(
        Comment, slug=comment_slug, project=project, deleted_at=None
    )
    return render(
        request,
        "comments/reply_form.html",
        {
            "parent_comment": parent_comment,
            "project": project,
        },
    )
