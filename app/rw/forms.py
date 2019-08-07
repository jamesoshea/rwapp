from django.forms import ModelForm, DateInput, TimeInput, Form, TextInput, Textarea, EmailInput, NumberInput
from django import forms
from rw.models import Event, BikeDonation, Collection, LandingContent, News
from django.utils.translation import gettext
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['date']
        widgets = {
            'date': DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Please select date of event'}),
        }


class LandingContentForm(ModelForm):
    class Meta:
        model = LandingContent
        fields = ['text', 'link']
        widgets = {
            'text': TextInput(
                attrs={'class': 'form-control',
                       'placeholder': gettext('Text')}),
            'link': TextInput(
                attrs={'class': 'form-control',
                       'placeholder': gettext('Link')}),
        }


class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = ['date', 'capacity']
        widgets = {
            'date': DateInput(
                attrs={'type': 'date', 'class': 'form-control',
                       'placeholder': gettext('Date')}),
            'capacity': NumberInput(
                attrs={'class': 'form-control', 'placeholder': gettext('vehicle capacity')}),
        }


class BikeDonationForm(ModelForm):
    class Meta:
        model = BikeDonation
        fields = ['name', 'email', 'phone', 'address', 'zip', 'latest_pickup', 'bike_count', 'message']
        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'placeholder': gettext('Name')}),
            'email': EmailInput(
                attrs={'class': 'form-control', 'placeholder': gettext('Email')}),
            'phone': TextInput(
                attrs={'class': 'form-control', 'placeholder': gettext('Phone')}),
            'address': TextInput(
                attrs={'class': 'form-control', 'placeholder': gettext('Address')}),
            'zip': TextInput(
                attrs={'class': 'form-control', 'placeholder': gettext('Postal code')}),
            'latest_pickup': DateInput(
                attrs={'type': 'date', 'class': 'form-control',
                       'placeholder': gettext('When is the latest possible pickup for you?')}),
            'bike_count': NumberInput(
                attrs={'class': 'form-control', 'placeholder': gettext('How many bikes to pickup?')}),
            'message': Textarea(
                attrs={'class': 'form-control', 'placeholder': gettext('Your message to us')}),
        }


class ContactForm(Form):
    name = forms.CharField(label=gettext('Name'),max_length=100, widget=TextInput(
        attrs={'class': 'form-control',}
    ))
    email = forms.EmailField(label = gettext('Email'),max_length=100, widget=EmailInput(
        attrs={'class': 'form-control', }
    ))
    phone = forms.CharField(label = gettext('Phone'),max_length=100, widget=TextInput(
        attrs={'class': 'form-control', }
    ))
    message = forms.CharField(label = gettext('Your message to us'),max_length=2000, widget=Textarea(
        attrs={'class': 'form-control', 'rows': '4', }
    ))

    class Meta:
        widgets = {
        }

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['image', 'date', 'headline', 'text',]
        widgets = {
            'text': TextInput(
                attrs={'class': 'form-control',
                       'placeholder': gettext('Newstext')}),
        }