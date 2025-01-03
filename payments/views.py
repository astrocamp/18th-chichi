from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Order
import json


@csrf_exempt
def payment_notify(request):
    if request.method == "POST":
        notify_data = request.POST.dict()

        try:
            order = Order.objects.get(order_id=notify_data.get("MerchantTradeNo"))

            if notify_data.get("RtnCode") == "1":
                order.paid = True
                order.save()

            return HttpResponse("1|OK")
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)

    return HttpResponse("Bad Request", status=400)


def payment_complete(request):
    return render(request, "payments/complete.html")
