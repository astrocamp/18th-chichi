from django.shortcuts import render, redirect, get_object_or_404
from .forms import PledgesForm
from .models import Pledges


# Create your views here.
def index(request):
    if request.POST:
        form = PledgesForm(request.POST)
        form.save()
        redirect("pledges:index")
    pledges = Pledges.objects.all()
    return render(request, "pledges/index.html", {"pledges": pledges})


def new(request):
    form = PledgesForm()
    return render(
        request,
        "pledges/new.html",
        {"form": form},
    )


def show(request, id):
    pledge = get_object_or_404(Pledges, id=id)
    if request.POST:
        form = PledgesForm(request.POST, instance=pledge)
        form.save()
        return redirect("pledges:index")
    return render(
        request,
        "pledges/show.html",
        {
            "pledge": pledge,
        },
    )


def delete(request, id):
    pledge = get_object_or_404(Pledges, id=id)
    if request.POST:
        pledge.delete()
        return redirect("pledges:index")
    return render(request, "pledges/delete.html", {"pledge": pledge})
