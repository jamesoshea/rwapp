from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum, Count
from django.http import JsonResponse
from rw.models import Order

# Aggregates the orders and bikes on a monthly basis and return a Json
def order_intake_per_month(request, *args, **kwargs):
    orders = Order.objects \
        .annotate(month=ExtractMonth('date_ordered'),
                  year=ExtractYear('date_ordered')) \
        .values('month', 'year') \
        .annotate(count=Count('pk')) \
        .annotate(bikes=Sum('bikes'))

    labels = []
    orders_count = []
    bikes_count = []

    for order in orders:
        month = str(order['month'])
        year = str(order['year'])
        order_count = order['count']
        bike_count = order['bikes']

        labels.append(year + "-" + month)
        orders_count.append(order_count)
        bikes_count.append(bike_count)

    data = {"labels": labels,
            "orders_count": orders_count,
            "bikes_count": bikes_count,
            }

    return JsonResponse(data, safe=False)
