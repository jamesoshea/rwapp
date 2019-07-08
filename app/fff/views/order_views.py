from django.shortcuts import render
from fff.models import Order

def orders(request):
  template_name = "order/orders.html"
  orders = Order.objects.all()

  context = {
  "orders" : orders
  }

  return render (request, template_name, context)
