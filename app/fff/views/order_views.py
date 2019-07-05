from django.shortcuts import render
from fff.models import Order

def orders(request):
  template_name = "order/orders.html"
  orders = Order.objects.all()

  context = {
  "orders" : orders
  }

  return render (request, template_name, context)

def order_new(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        bikes = request.POST['bikes']
        order_type = request.POST.get('order_type')
        print (str(order_type))
        note = request.POST['note']
        order = Order(name=name,
                      email=email,
                      phone=phone,
                      bikes=bikes,
                      note=note,
                      order_type=order_type )
        order.status = "ORDERED"
        order.date_ordered = date.today()
        order.save()
        return redirect('order_new')
    else:
        return render(request, 'order/order_new.html')
