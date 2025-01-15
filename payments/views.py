from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Order
from anymail.message import AnymailMessage
from django.utils import timezone
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
                send_success_email(order)

            return HttpResponse("1|OK")
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)

    return HttpResponse("Bad Request", status=400)


def send_success_email(order):

    user_profile = order.user.profile
    project = order.reward.project if order.reward else None

    local_created_at = timezone.localtime(order.created_at)
    formatted_amount = "{:,.2f}".format(order.amount)

    message = AnymailMessage(
        subject="贊助成功",
        to=[order.user.email],
    )
    message.template_id = "sponsorship_success"
    message.merge_global_data = {
        "order_id": order.order_id,
        "amount": formatted_amount,
        "description": order.description,
        "created_at": local_created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "user_name": order.user.username,
        "user_email": order.user.email,
        "user_phone": user_profile.phone if user_profile.phone else "",
        "project_title": project.title if project else "自由贊助",
        "reward_title": order.reward.title if order.reward else "自由贊助",
        "reward_price": ("{:,.2f}".format(order.reward.price) if order.reward else formatted_amount),
        "estimated_delivery": (order.reward.estimated_delivery.strftime("%Y-%m-%d") if order.reward else ""),
    }
    message.send()

def payment_complete(request):
    return render(request, "payments/complete.html")
