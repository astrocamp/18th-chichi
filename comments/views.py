from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from projects.models import Project
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.template.loader import render_to_string
from django.http import HttpResponse


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

    return render(request, "comments/new.html", {"project": project})


@login_required
def show(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    project = comment.project
    if request.POST:
        content = request.POST.get("content")
        if content:
            new_comment = Comment.objects.create(
                content=content,
                project=project,
                account=request.user,
                parent=comment,
            )
            if request.headers.get("HX-Request") == "true":
                # 如果是 HTMX 請求，返回新回覆的局部HTML，不需整個網頁刷新
                html = render_to_string(
                    "comments/reply.html",
                    {"reply": new_comment},
                    request=request,
                )
                return HttpResponse(html)

            return redirect("comments:show", slug=comment.slug)

    # 獲取該評論的所有回覆
    replies = comment.replies.all().order_by("-created_at").select_related("account")

    return render(
        request,
        "comments/show.html",
        {
            "comment": comment,
            "replies": replies,
            "project": project,
        },
    )


@login_required
def delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    project = get_object_or_404(Project, id=comment.project.id)

    if request.method == "POST":
        comment.delete()
        if request.headers.get("HX-Request") == "true":
            return HttpResponse()
        else:  # 如果不是 HTMX 請求，則根據評論是否有父評論進行重定向：

            if comment.parent:
                return redirect("comments:show", id=comment.parent.id)
            else:
                return redirect("projects:comment_index", id=project.id)

    return render(request, "comments/delete.html", {"comment": comment})
