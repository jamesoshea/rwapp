from datetime import date

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.utils.translation import gettext

from fff.forms import ContactForm, LandingContentForm, NewsForm
from fff.models import Order, LandingContent

def add_landing_content(request):
    landing_content = LandingContent.objects.all()[0]
    landing_content_form = LandingContentForm(request.POST or None, instance = landing_content)

    if(request.method == "POST"):
        landing_content_form.save()

    context = {
        'landing_content_form': landing_content_form,
    }
    return render(request, 'add_landing_content.html', context)

def add_news(request):
    news_form = NewsForm(request.POST or None, request.FILES or None)
    print (request.POST)
    print (news_form.is_valid())
    if news_form.is_valid():
        news_form.save()
    else:
        print (news_form)
        print ("failed")
        pass

    context = {
        'news_form': news_form,
    }
    return render(request, 'add_news.html', context)


def website(request):
    contact_form = ContactForm(request.POST or None)
    landing_content = LandingContent.objects.all()[0]

    if contact_form.is_valid():
        process_contact_form(contact_form)

    context = {
        'contact_form': contact_form,
        'landing_content': landing_content,
    }
    return render(request, 'website/index.html', context)

def website_order(request):
    template_name = 'website/bike_order.html'
    success_template = 'website/bike_order_success.html'

    if (request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        bikes = request.POST['bikes']
        note = request.POST['note']
        order_type = request.POST['order_type']
        order = Order(name=name,
                      email=email,
                      phone=phone,
                      bikes=bikes,
                      note=note,
                      order_type = order_type, )
        order.status = "ORDERED"
        order.date_ordered = date.today()
        order.save()
        #order.send_order_saved_mail()
        return render(request, success_template)
    else:
        return render(request, template_name)

def process_contact_form(contact_form):
  subject = gettext('contact_form_email_subject')
  name = contact_form.cleaned_data['name']
  email = contact_form.cleaned_data['email']
  phone = contact_form.cleaned_data['phone']
  form_message = contact_form.cleaned_data['message']
  to = ['jakobschult@yahoo.de']

  message = "<html>" \
            "Hello, <br>" \
            "<br>" \
            "folgende Nachricht wurde über die Internetseite an uns gesendet:<br><br>" \
            "Von: " + name + "<br>" \
                             "Email: " + email + "<br>" \
                                                 "Phone: " + phone + "<br>"
  email_message = EmailMultiAlternatives(subject=subject, from_email="info@rueckenwind.berlin", to=to,
                                         headers={'Reply-To': email})
  email_message.attach_alternative(message, "text/html")
  email_message.send()
  messages.success(request, 'Form submission successful')
