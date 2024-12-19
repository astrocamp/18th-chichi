from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProjectFrom
from .models import Project
from django.utils.timezone import localtime
from django.utils import timezone

def index(request):
    if request.POST:
        form = ProjectFrom(request.POST)
        form.save()
        return redirect("projects:index")
    
    projects = Project.objects.all()
    return render(request, "projects/index.html", {"projects":projects})


def new(request):
    return render(request, "projects/new.html",)



def show(request, id):
    project = get_object_or_404(Project,id=id)
    if request.POST:
        form = ProjectFrom(request.POST, instance=project)
        form.save()
        project.update_at = timezone.now()
        project.save()
        return redirect("projects:show", id = project.id)
    

    return render(request, "projects/show.html",{"project":project})




def edit(request, id):
    project = get_object_or_404(Project,id=id)

    format_time_start =localtime(project.start_at).strftime('%Y-%m-%dT%H:%M')
    format_time_end =localtime(project.end_at).strftime('%Y-%m-%dT%H:%M')
    return render(request, "projects/edit.html",{"project":project,
"format_time_start":format_time_start,"format_time_end":format_time_end})


def delete(request, id):
    project = get_object_or_404(Project,id=id)
    if request.POST:
        project.delete()

        return redirect("projects:index")

    return render(request, "projects/delete.html",)