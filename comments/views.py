from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from projects.models import Project
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST


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
    comments = (
        Comment.objects.filter(parent__isnull=True, project=project)
        .order_by("-created_at")
        .select_related(
            "account", "project"
        )  # 預先載入與 Comment 相關的 account 及 project 物件，避免後續因為存取屬性再做多次查詢
    )

    return render(
        request, "comments/index.html", {"comments": comments, "project": project}
    )


@login_required
def new(request, slug):
    project = get_object_or_404(Project, slug=slug)
    comments = project.comments.all().order_by("-created_at")  # 按時間降序排列留言

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
            # 如果留言內容為空，返回錯誤
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
            # 创建回复
            new_reply = Comment.objects.create(
                project=project,
                content=content,
                account=request.user,
                parent=parent_comment,
            )
            # 如果是 HTMX 请求，返回部分模板
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
def load_reply_form(request, slug, comment_slug):
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
