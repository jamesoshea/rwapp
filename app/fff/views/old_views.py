from fff.forms import EventForm, ContactForm, BikeDonationForm, CollectionForm, LandingContentForm, NewsForm
from fff.models import Order, Event, Bike, User, LandingContent, BikeDonation, Collection, News
from datetime import date
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum, Count, Q
from django.utils.translation import gettext
from django.contrib import messages
from django.views.generic import ListView


class BikeDonationListView(ListView):
    model = BikeDonation
    template_name = "donations.html"

    def get_queryset(self):
        donations = BikeDonation.objects.values('date_input', 'zip', 'latest_pickup', 'bike_count', 'status')
        return donations

def donations(request):
    context = {
        'donations_values': BikeDonation.objects.values('date_input', 'zip', 'latest_pickup', 'bike_count', 'status', 'pk'),
        'donations': BikeDonation.objects.all()
    }
    return render(request, 'donations.html', context)


class OrderListView(ListView):
    model = Order
    template_name = "orders.html"

    def get_queryset(self):
        orders = Order.objects.values('name', 'bikes', 'date_input', 'status', 'event')
        return orders


class CollectionListView(ListView):
    model = Order
    template_name = "collections.html"

    def get_queryset(self):
        collections = Collection.objects.values('date', 'capacity')
        return collections


def add_donation(request):
    bike_donation_form = BikeDonationForm(request.POST or None)

    if bike_donation_form.is_valid():
        bike_donation = bike_donation_form.save(commit=False)
        bike_donation.geocode()
        bike_donation.date_input = date.today()
        bike_donation.save()
        return redirect('donations')
    context = {
        'bike_donation_form': bike_donation_form,
    }
    return render(request, 'add_donation.html', context)


def website_team(request):
    context = {

    }
    return render(request, 'website/team.html', context)


def website_news(request):
    news = News.objects.all().order_by('-date')
    context = {
        'news': news,
    }
    return render(request, 'website/news.html', context)


def website_donate(request):
    return redirect(
        "https://www.betterplace.org/de/projects/61457-jeden-tag-ein-fahrrad-fur-gefluchtete-unser-ziel-in-2018/")


def events(request):
    events = Event.objects.filter(date__gte=date.today()).order_by('date')
    past_events = Event.objects.filter(date__lt=date.today()).order_by('date')
    context = {
        'events': events,
        'past_events': past_events,
    }
    return render(request, 'events.html', context)


def bike_remove(request, bike_id):
    bike = Bike.objects.get(id=bike_id)
    order_hashed_id = bike.order.hashed_id
    bike.remove_order()
    bike.save()
    return redirect("/fff/order/" + order_hashed_id + "/fulfill")


def volunteer_events(request, volunteer_id):
    if (request.method == 'POST'):
        volunteer = User.objects.get(id=volunteer_id)
        event = Event.objects.get(id=request.POST['event_id'])
        if request.POST['operation'] == "remove":
            event.volunteers.remove(volunteer)
        elif request.POST['operation'] == "add":
            event.volunteers.add(volunteer)
        event.save()
    events = list(Event.objects.order_by('date'))
    volunteer_events = Event.objects.filter(volunteers__id=volunteer_id).extra(order_by=['date'])

    for volunteer_event in volunteer_events:
        events.remove(volunteer_event)

    context = {
        'events': events,
        'volunteer_events': volunteer_events,
        'volunteer_id': volunteer_id,
    }
    return render(request, 'volunteer_events.html', context)


class AddOrderToEvent(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs["event_id"])
        orders = Order.objects.order_by('date_input')
        context = {
            "orders": orders,
            "event": event,
        }
        return render(request, "add_order_to_event_2.html", context)

    def post(self, request, *args, **kwargs):

        if request.POST['operation'] == "plan":
            order = Order.objects.get(id=request.POST['order_id'])
            event.volunteers.remove(volunteer)
            order.plan(event)
            order.save()

        for order_id in request.POST.getlist("orders"):
            order = Order.objects.get(id=order_id)
            order.plan(event)
            order.save()
        event.save()
        return redirect("/event/" + str(kwargs["event_id"]))  # warum muss ich das hier machen


def add_order_to_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if (request.method == 'POST'):
        for email in request.POST.getlist("orders"):
            order = Order.objects.get(email=email)
            order.plan(event)
            order.save()
        event.save()
        return redirect("/event/" + str(event_id))  # warum muss ich das hier machen? Muss man nicht :)
    orders = Order.objects.filter(
        Q(status="ORDERED") | Q(status="PLANNED") | Q(status="INVITED") | Q(status="DECLINED")).order_by('date_ordered')
    context = {
        "orders": orders,
        "event": event,
    }
    return render(request, "add_order_to_event_2.html", context)


def index(request):
    if (request.method == 'POST'):
        event_id = request.POST['event_id']
        event = Event.objects.get(id=event_id)
        for order_id in request.POST.getlist("orders"):
            order = Order.objects.get(id=order_id)
            order.plan(event)

            order.save()
        event.save()
        return redirect('/event/' + event_id)
    orders = Order.objects.all()
    events = Event.objects.all()
    context = {
        'orders': orders,
        'events': events,
    }
    return render(request, 'index.html', context)


def order_confirm(request, hashed_id):
    order = Order.objects.filter(hashed_id=hashed_id)
    event_id = 0
    for o in order:
        event_id = o.event.pk
        o.confirm()
        o.save()
    context = {
        'order': order,
    }
    return render(request, 'order_confirm.html', context)


def order_invite(request, hashed_id):
    order = Order.objects.filter(hashed_id=hashed_id)
    event_id = 0
    for o in order:
        event_id = o.event.pk
        o.invite()
        o.save()
    return redirect('/event/' + str(event_id))


def order_decline(request, hashed_id):
    order = Order.objects.filter(hashed_id=hashed_id)
    event_id = 0
    for o in order:
        event_id = o.event.pk
        o.decline()
        o.save()
    return redirect('/event/' + str(event_id))


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {
        'order': order
    }
    return render(request, 'details.html', context)


def order_fulfill(request, hashed_id):
    order = Order.objects.get(hashed_id=hashed_id)

    if request.method == "POST":
        bike = Bike()
        bike.manufacturer = request.POST.get('bike_manufacturer')
        bike.frame_number = request.POST.get('bike_frame_number')
        bike.color = request.POST.get('bike_color')

        order = Order.objects.get(hashed_id=hashed_id)
        order.fulfill()
        order.save()
        bike.order = order
        bike.save()
        bikes = Bike.objects.filter(order=order)
        context = {
            'order': order,
            'bikes': bikes,
        }
        return render(request, 'order_fulfill.html', context)
    else:
        bikes = Bike.objects.filter(order=order)
        context = {
            'order': order,
            'bikes': bikes,
        }
        return render(request, 'order_fulfill.html', context)


def order_plan(request, hashed_id):
    order = Order.objects.get(hashed_id=hashed_id)
    current_event_id = order.event.pk
    events = Event.objects.order_by('date')

    if request.method == "POST":
        selected_event = Event.objects.get(pk=request.POST["eventSelect"])
        order.status = "PLANNED"
        order.event = selected_event
        order.save()
        return redirect('/event/' + request.POST["eventSelect"])

    context = {

        "hashed_id": hashed_id,
        "current_event_id": current_event_id,
        "events": events,
    }

    return render(request, "order_plan.html", context)


def order_remove(request, hashed_id):
    order = Order.objects.get(hashed_id=hashed_id)  #
    event_id = order.event.pk
    order.event = None

    #  update status information
    if order.status == "PLANNED":
        order.status = "ORDERED"
    if order.status == ("INVITED" or "CONFIRMED") :
        order.status = "ORDERED"
        #mail_factory.send_mail(WE are very sorry. WE had to cancel the event. Can you come on the ?)
    if order.status == "DECLINED":
        order.status = "DECLINED"
    order.save()
    return redirect("/event/" + str(event_id))


def add_event(request):
    add_event_form = EventForm(request.POST or None)

    if add_event_form.is_valid():
        new_event = add_event_form.save()
        return redirect('/event/' + str(new_event.pk))

    context = {
        'event_form': add_event_form,
    }
    return render(request, 'add_event.html', context)


def add_collection(request):
    add_collection_form = CollectionForm(request.POST or None)

    if add_collection_form.is_valid():
        new_collection = add_collection_form.save()
        return redirect('/collections')

    context = {
        'collection_form': add_collection_form,
    }
    return render(request, 'add_collection.html', context)


def event_delete(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('/events/')


def event_invite_all(request, event_id):
    event = Event.objects.get(pk=event_id)
    for order in Order.objects.filter(event=event):
        order.invite()
        order.save()
    return redirect('/event/' + str(event_id))


@login_required
def event(request, event_id):
    event = Event.objects.get(id=event_id)
    if (request.method == 'POST'):
        for volunteer_id in request.POST.getlist("volunteers"):
            volunteer = User.objects.get(id=volunteer_id);
            event.volunteers.add(volunteer)
            event.save()
        return redirect('/event/' + event_id)
    else:
        orders = Order.objects.filter(event=event)
        volunteers = User.objects.all
        event_volunteers = event.volunteers.all()
        context = {
            'orders': orders,
            'ordercount': orders.count(),
            'event': event,
            'volunteers': volunteers,
            'event_volunteers': event_volunteers,
        }
        return render(request, 'event.html', context)
