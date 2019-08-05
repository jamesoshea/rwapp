import googlemaps
import hashlib

from datetime import date, datetime

from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.utils.translation import gettext

from rw.app_config import *
from fff.functions import EmailService


class Collection(models.Model):
    date = models.DateField(
        blank=True, null=True, help_text="When do you want to collect the bicycles"
    )
    capacity = models.IntegerField(
        blank=True, null=True, help_text="How many bikes can be collected?"
    )

    def __str__(self):
        return self.date


class BikeDonation(models.Model):
    date_input = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    latest_pickup = models.DateField(max_length=50, blank=True, null=True)
    bike_count = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True, max_length=300)
    status = models.TextField(blank=True, null=True)
    collection = models.ForeignKey(
        Collection, blank=True, null=True, on_delete=models.SET_NULL
    )
    latitude = models.CharField(max_length=13, blank=True, null=True)
    longitude = models.CharField(max_length=13, blank=True, null=True)

    def geocode(self):
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API)
        # Geocoding an address
        geocode_result = gmaps.geocode(self.address + ", " + self.zip)
        if len(geocode_result):
            location = geocode_result[0]["geometry"]["location"]
            self.latitude = location["lat"]
            self.longitude = location["lng"]
        else:
            self.latitude = 0
            self.longitude = 0

    def save(self, *args, **kwargs):
        self.geocode()
        super(BikeDonation, self).save(
            *args, **kwargs
        )  # Call the "real" save() method.

    def __str__(self):
        return self.name


class LandingContent(models.Model):
    text = models.CharField(
        help_text="What should be displayed in the box on the homepage?", max_length=50
    )
    link = models.URLField(
        help_text="What should be displayed in the box on the homepage?"
    )

    def __str__(self):
        return self.text


class News(models.Model):
    image = models.ImageField(blank=True, null=True)
    date = models.DateField(
        help_text="The date that will be shown on the website as the date of this news entry",
        default=datetime.now,
    )
    headline = models.CharField(max_length=200, default="")
    text = models.TextField(default="")

    def __str__(self):
        return "" + str(self.date) + " " + str(self.headline)


class User(AbstractUser):
    phone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Event(models.Model):
    date = models.DateField(
        blank=True, null=True, help_text="When do you want to repair?"
    )
    capacity = models.IntegerField(
        blank=True, null=True, help_text="How many bikes can be repaired?"
    )
    volunteers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return "" + str(self.date)

    def get_planned_bikes(self):
        result = 0
        for order in self.order_set.all():
            result = result + int(order.bikes)
        return result

    def get_all_volunteers(self):
        result = ""
        for volunteer in self.volunteers.all():
            result = result + "    " + volunteer.username
        return result


class Order(models.Model):
    CANCEL_REASONS = (
        ("NOREASON", gettext("No reason")),
        ("TOOLONG", gettext("Too long")),
        ("OTHERBIKE", gettext("Other bike")),
    )

    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100)
    order_type = models.CharField(blank=True, null=True, max_length=100)
    bikes = models.IntegerField(
        help_text=gettext("How many bikes are we talking about?"), null=True
    )
    bikes_fulfilled = models.IntegerField(blank=True, null=True)
    date_ordered = models.DateField(
        blank=True, null=True, help_text=gettext("Date at which the order was placed")
    )
    phone = models.CharField(max_length=30, blank=True, null=True)
    note = models.CharField(max_length=300, blank=True, null=True)
    date_invited = models.DateField(blank=True, null=True)
    date_answered = models.DateField(blank=True, null=True)
    date_repaired = models.DateField(blank=True, null=True)
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=30, blank=True, null=True)
    hashed_id = models.CharField(max_length=256)
    cancel_reason = models.CharField(
        max_length=30, choices=CANCEL_REASONS, default="NOREASON"
    )

    def save(self):
        self.hashed_id = hashlib.sha256(str(self.email).encode("utf-8")).hexdigest()
        super(Order, self).save()

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.email

    def plan(self, event):
        self.bikes_fulfilled = 0

        if event is None:
            return
        else:
            self.status = "PLANNED"
            self.event = event

    def planable(self):
        return (
            self.status == "ORDERED"
            or self.status == "DECLINED"
            or self.status == "PLANNED"
        )

    def invite(self, request):
        self.status = "INVITED"
        self.date_invite = date.today()
        email_service = EmailService()
        email_service.send_order_invite(self, self.event, request)

    def confirm(self):
        self.status = "CONFIRMED"
        self.date_answered = date.today()
        self.save()

    def decline(self):
        self.status = "DECLINED"
        self.date_answered = date.today()
        self.save()

    def delete(self):
        self.status = "DELETED"
        self.save()

    def cancel(self):
        self.status = "CANCELED"
        self.save()

    def fulfill(self):
        self.bikes_fulfilled = self.bikes_fulfilled + 1
        if int(self.bikes_fulfilled) >= int(self.bikes):
            self.status = "FULFILLED"
        self.save()

    def remove_bike(self):
        self.bikes_fulfilled = self.bikes_fulfilled - 1
        if self.status == "DECLINED" or self.status == "INVITED":
            self.status = "ORDERED"
        self.save()


class Bike(models.Model):
    manufacturer = models.CharField(max_length=30, blank=True, null=True)
    frame_number = models.CharField(max_length=30, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE)

    def remove_order(self):
        self.order.remove_bike()
        self.order = None
        self.delete()


class SupportingMember(models.Model):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    mail = models.EmailField()
    phone = models.CharField(max_length=100)
    newsletter = models.BooleanField()
    amount = models.IntegerField()
    iban = models.CharField(max_length=100)
    bic = models.CharField(max_length=90)
    sepa = models.BooleanField()
    date_signup = models.DateField()

