from django.shortcuts import render,redirect,get_object_or_404
from .forms import UpdateRecordFrom
from .models import UpdateRecord
from django.utils import timezone

def index(request):
    if request.POST:
        form = UpdateRecordFrom(request.POST)
        form.save()
        return redirect("update_records:index")
    
    update_records = UpdateRecord.objects.all()
    return render(request, "update_records/index.html", {"update_records":update_records})


def new(request):
    return render(request, "update_records/new.html",)



def show(request, id):
    update_record = get_object_or_404(UpdateRecord,id=id)
    if request.POST:
        form = UpdateRecordFrom(request.POST, instance=update_record)
        form.save()
        update_record.update_at = timezone.now()
        update_record.save()
        return redirect("update_records:show", id = update_record.id)
    

    return render(request, "update_records/show.html",{"update_record":update_record})




def edit(request, id):
    update_record = get_object_or_404(UpdateRecord, id=id)
    return render(request, "update_records/edit.html",{"update_record":update_record})


def delete(request, id):
    update_record = get_object_or_404(UpdateRecord,id=id)
    if request.POST:
        update_record.delete()

        return redirect("update_records:index")

    return render(request, "update_records/delete.html",)