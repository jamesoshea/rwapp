from django.contrib import admin

from .models import Order,Event,Bike, User, LandingContent, BikeDonation, News, SupportingMember

admin.site.register(Order)
admin.site.register(Event)
admin.site.register(Bike)
admin.site.register(User)
admin.site.register(LandingContent)
admin.site.register(BikeDonation)
admin.site.register(News)
admin.site.register(SupportingMember)
