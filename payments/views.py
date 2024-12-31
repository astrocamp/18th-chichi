from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Order
from .ecpay_sdk import ECPayPayment
from datetime import datetime
import json


def create_payment(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description", "商品訂單")
        order_id = f"TEST{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order = Order.objects.create(
            order_id=order_id, amount=amount, description=description
        )
        ecpay = ECPayPayment()
        order_params = ecpay.create_order(
            order_id=order_id, amount=amount, description=description
        )
        return render(
            request,
            "payments/checkout.html",
            {"payment_url": ecpay.payment_url, "order_params": order_params},
        )

    return render(request, "payments/create_payment.html")


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
