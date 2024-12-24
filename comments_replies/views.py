from django.shortcuts import render, redirect, get_object_or_404
from .models import CommentsReplies
from django.utils import timezone


def index(request):
    if request.POST:
        comments_reply = CommentsReplies()
        comments_reply.content = request.POST.get("content")
        comments_reply.save()
        return redirect("comments_replies:index")

    comments_replies = CommentsReplies.objects.filter(account=request.user)
    CommentsReplies.objects.create(content="content", account=request.user)
    return render(
        request,
        "comments_replies/index.html",
        {"comments_replies": comments_replies},
    )


def new(request):
    return render(request, "comments_replies/new.html")


def show(request, id):
    comments_reply = get_object_or_404(CommentsReplies, id=id)
    if request.POST:
        comments_reply.content = request.POST.get("content")
        comments_reply.update_at = timezone.now()
        comments_reply.save()
        return redirect("comments_replies:show", id=comments_reply.id)

    return render(
        request,
        "comments_replies/show.html",
        {"comments_reply": comments_reply},
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
    if request.POST:
        comments_reply.delete()
        return redirect("comments_replies:index")

    return render(
        request,
        "comments_replies/delete.html",
        {"comments_reply": comments_reply},
    )
