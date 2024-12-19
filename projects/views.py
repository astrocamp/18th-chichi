from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProjectFrom
from .models import Project
from django.utils.timezone import localtime
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request, id):
    account = get_object_or_404(User, id=id)
    if request.POST:
        form = ProjectFrom(request.POST) 
        if form.is_valid():
            project = form.save(commit=False)
            project.account = account
            project.save()
            return redirect("accounts:projects" , id = account.id)
        else:
            return HttpResponse("輸入錯誤")

    projects = Project.objects.filter(account=account)
    return render(request, "projects/index.html", {"projects":projects,"account":account})
        

def new(request,id):
    account = get_object_or_404(User, id=id)
    return render(request, "projects/new.html",{"account":account})




def show(request, id):
    project = get_object_or_404(Project,id=id)
    account = get_object_or_404(User, id=request.user.id)

    if request.POST:
        form = ProjectFrom(request.POST, instance=project)
        form.save()
        project.update_at = timezone.now()
        project.save()
        return redirect("projects:show", id = project.id)
    

    return render(request, "projects/show.html",{"project":project,"account":account})




def edit(request, id):
    project = get_object_or_404(Project,id=id)

    format_time_start =localtime(project.start_at).strftime('%Y-%m-%dT%H:%M')
    format_time_end =localtime(project.end_at).strftime('%Y-%m-%dT%H:%M')
    return render(request, "projects/edit.html",{"project":project,
"format_time_start":format_time_start,"format_time_end":format_time_end})


def delete(request, id):
    project = get_object_or_404(Project,id=id)
    account = get_object_or_404(User, id=request.user.id)
    if request.POST:
        project.delete()

        return redirect("accounts:projects", id = account.id )

    return render(request, "projects/delete.html",)