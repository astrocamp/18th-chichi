from django.shortcuts import render, redirect, get_object_or_404
from .models import CommentsReplies
from django.utils import timezone
from comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def index(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    if request.POST:
        comments_reply = CommentsReplies()
        comments_reply.content = request.POST.get("content")
        comments_reply.comment = comment
        comments_reply.account = request.user

        comments_reply.save()
        return redirect("comments:comments_replies_index", slug=comment.slug)

    comments_replies = CommentsReplies.objects.filter(comment=comment)
    return render(
        request,
        "comments_replies/index.html",
        {"comments_replies": comments_replies, "comment": comment},
    )


@login_required
def new(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    return render(request, "comments_replies/new.html", {"comment": comment})


@login_required
def show(request, id):
    comments_reply = get_object_or_404(CommentsReplies, id=id)
    comment = comments_reply.comment

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


@login_required
def edit(request, id):
    comments_reply = get_object_or_404(CommentsReplies, id=id)
    comment = comments_reply.comment
    return render(
        request,
        "comments_replies/edit.html",
        {"comments_reply": comments_reply, "comment": comment},
    )


@login_required
def delete(request, id):
    comments_reply = get_object_or_404(CommentsReplies, id=id)
    comment = comments_reply.comment

    if request.POST:
        comments_reply.delete()
        return redirect("comments:comments_replies_index", slug=comment.slug)

    return render(
        request,
        "comments_replies/delete.html",
        {"comments_reply": comments_reply, "comment": comment},
    )
