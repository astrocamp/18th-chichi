from django.shortcuts import render,redirect,get_object_or_404
from .forms import UpdateRecordFrom
from .models import UpdateRecord
from projects.models import Project
from django.utils import timezone


def index(request, id):
    project = get_object_or_404(Project, id=id)
    
    if request.method == "POST":
        UpdateRecord.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            project=project
        )
        return redirect("update_records:index", id=id)
    
    update_records = UpdateRecord.objects.filter(project=project)
    return render(request, "update_records/index.html", {
        "update_records": update_records,
        "project": project,
        "id": id
    })

def new(request, id):
    return render(request, "update_records/new.html", {"id": id})



def show(request, id, update_id):
    project = get_object_or_404(Project, id=id)
    update_record = get_object_or_404(UpdateRecord, id=update_id, project=project)
    
    if request.POST:
        form = UpdateRecordFrom(request.POST, instance=update_record)
        form.save()
        update_record.update_at = timezone.now()
        update_record.save()
        return redirect("update_records:show", id=id, update_id=update_record.id)
    
    return render(request, "update_records/show.html", {
        "update_record": update_record,
        "id": id
    })




def edit(request, id, update_id):
    project = get_object_or_404(Project, id=id)
    update_record = get_object_or_404(UpdateRecord, id=update_id, project=project)
    return render(request, "update_records/edit.html",{"update_record":update_record,"id":id,})


def delete(request, id, update_id):
    update_record = get_object_or_404(UpdateRecord,id=update_id)
    if request.POST:
        update_record.delete()

        return redirect("update_records:index" ,id=id)

    return render(request, "update_records/delete.html",{
        "update_record": update_record,
        "id": id        
    })