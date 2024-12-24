from django.shortcuts import render,redirect,get_object_or_404
from .forms import UpdateRecordFrom
from .models import UpdateRecord
from projects.models import Project
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def index(request, id):
    project = get_object_or_404(Project, id=id)
    
    if request.method == "POST":
        UpdateRecord.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            project=project
        )
        return redirect("projects:update_records_index", id=project.id)
    
    update_records = UpdateRecord.objects.filter(project=project)
    return render(request, "update_records/index.html", {
        "update_records": update_records,
        "project": project,
        "id": id
    })

def new(request, id):
    return render(request, "update_records/new.html", {"id": id})



def show(request, update_id):
    update_record = get_object_or_404(UpdateRecord, id=update_id)
    project_id = update_record.project.id 
    
    if request.POST:
        form = UpdateRecordFrom(request.POST, instance=update_record)
        form.save()
        update_record.update_at = timezone.now()
        update_record.save()
        return redirect("update_records:show", update_id=update_record.id)
    
    return render(request, "update_records/show.html", {
        "update_record": update_record,
        "id": project_id
    })




def edit(request, update_id):
    update_record = get_object_or_404(UpdateRecord, id=update_id)
    project_id = update_record.project.id  
    
    return render(request, "update_records/edit.html", {
        "update_record": update_record,
        "id": project_id
    })


def delete(request, update_id):
    update_record = get_object_or_404(UpdateRecord, id=update_id)
    project_id = update_record.project.id  
    
    if request.POST:
        update_record.delete()
        return redirect("projects:update_records_index", id=project_id)  

    return render(request, "update_records/delete.html", {
        "update_record": update_record,
        "id": project_id
    })