from django.shortcuts import render,redirect,get_object_or_404
from .models import Comment
from django.utils import timezone

def index(request):
    if request.POST:
        comment = Comment()
        comment.content = request.POST.get('content')
        comment.save()

        return redirect("comments:index")
    
    comments = Comment.objects.all()

    return render(request, "comments/index.html",{"comments":comments})


def new(request):
    return render(request, "comments/new.html")



def show(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.POST:
        comment.content = request.POST.get('content')
        comment.update_at = timezone.now()
        comment.save()
        return redirect("comments:show", id=comment.id)
    return render(request, "comments/show.html", {"comment":comment})

def edit(request, id):
    comment = get_object_or_404(Comment, id=id)
    return render(request, "comments/edit.html", {"comment":comment})

def delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.POST:
        comment.delete()
        return redirect("comments:index")
    return render(request, "comments/delete.html", {"comment":comment})