from django.shortcuts import render,redirect,get_object_or_404
from .models import Comment
from projects.models import Project
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
def index(request):
    comments = Comment.objects.filter(user=request.user)
    
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        
        if not content:
            return render(request, "comments/index.html", {
                "error": "Content cannot be empty",
                "comments": comments
            })
        
        project = Project.objects.filter(id=1).first()
        
        if not project:
            project = Project.objects.create(
                id=1,
                title="Default Project",
                description="This is a default project",
            )
        
        Comment.objects.create(
            content=content,
            user=request.user,
            project=project
        )
        return redirect('comments:index')
    
    return render(request, "comments/index.html", {"comments": comments})



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