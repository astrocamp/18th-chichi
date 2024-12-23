from django.shortcuts import render, redirect, get_object_or_404
from .models import CommentsReplies
from django.utils import timezone
from comments.models import Comment


def index(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.POST:
        comments_reply = CommentsReplies()
        comments_reply.content = request.POST.get("content")
        comments_reply.comment = comment  # 告訴程式這條回覆留言是屬於這條評論   #就是把你從資料庫中找到的「評論」（comment）這個物件，和「回覆」（comments_reply）連起來。
        comments_reply.save()
        return redirect("comments:comments_replies_index", id=comment.id)

    comments_replies = CommentsReplies.objects.filter(
        comment=comment
    )  # 從 CommentsReplies 表中找出所有屬性 comment 等於 comment 的回覆。
    # 這裡的 comment 是一個 Comment 模型的實例。
    return render(
        request,
        "comments_replies/index.html",
        {"comments_replies": comments_replies, "comment": comment},
    )


def new(request, id):
    comment = get_object_or_404(Comment, id=id)
    return render(request, "comments_replies/new.html", {"comment": comment})


def show(request, id):
    comments_reply = get_object_or_404(CommentsReplies, id=id)
    comment = get_object_or_404(Comment, id=comments_reply.comment.id)

    if request.POST:
        comments_reply.content = request.POST.get("content")
        comments_reply.update_at = timezone.now()
        comments_reply.save()
        return redirect("comments_replies:show", id=comments_reply.id)

    return render(
        request,
        "comments_replies/show.html",
        {
            "comments_reply": comments_reply,
            "comment": comment,
        },
    )


def edit(request, id):
    comments_reply = get_object_or_404(CommentsReplies, id=id)
    return render(
        request,
        "comments_replies/edit.html",
        {"comments_reply": comments_reply},
    )


def delete(request, id):
    comments_reply = get_object_or_404(CommentsReplies, id=id)
    comment = get_object_or_404(Comment, id=comments_reply.comment.id)
    if request.POST:
        comments_reply.delete()
        return redirect("comments:comments_replies_index", id=comment.id)

    return render(
        request,
        "comments_replies/delete.html",
        {"comments_reply": comments_reply, "comment": comment},
    )
