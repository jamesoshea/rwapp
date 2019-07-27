from django.shortcuts import render
from fff.models import Order


def orders(request):
    template_name = "order/orders.html"
    orders = Order.objects.all()

    context = {"orders": orders}

    return render(request, template_name, context)


def order_cancel(request, hashed_id):
    template_name = "order/order_canceled.html"

    order = Order.objects.get(hashed_id=hashed_id)
    order.cancel()

    context = {"order": order}
    return render(request, template_name, context)

