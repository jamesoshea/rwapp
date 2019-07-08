from datetime import date

from django.shortcuts import render, redirect
from django.utils.translation import gettext

from fff.forms import ContactForm, LandingContentForm, NewsForm, BikeDonationForm
from fff.functions import EmailService
from fff.models import Order, LandingContent, SupportingMember

def website(request):
    contact_form = ContactForm(request.POST or None)
    landing_content = LandingContent.objects.all()[0]
    template = 'website/index.html'
    form_success_template = 'website/form_success.html'

    if contact_form.is_valid():
      process_contact_form(contact_form)
      success_header = gettext('website_contactform_success_header')
      success_text = gettext('website_contactform_success_text')
      success_context = {
        'success_header': success_header,
        'success_text': success_text,
      }
      return render (request, form_success_template, success_context)

    context = {
        'contact_form': contact_form,
        'landing_content': landing_content,
    }
    return render(request, template, context)

def process_contact_form(contact_form):
  name = contact_form.cleaned_data['name']
  email = contact_form.cleaned_data['email']
  phone = contact_form.cleaned_data['phone']
  message = contact_form.cleaned_data['message']
  email_service = EmailService()
  email_service.send_contact_success(name, email, phone, message)

def update_landing_content(request):
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
    if news_form.is_valid():
        news_form.save()

    context = {
        'news_form': news_form,
    }
    return render(request, 'add_news.html', context)

def website_order(request):
    template_name = 'website/bike_order.html'
    success_template = 'website/form_success.html'

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
        success_header = gettext('website_bikeorder_success_header')
        success_text = gettext('website_bikeorder_success_text')
        success_context = {
          'success_header': success_header,
          'success_text': success_text,
        }
        #order.send_order_saved_mail()
        return render(request, success_template, success_context)
    else:
        return render(request, template_name)

def website_bikedonate(request):
  bike_donation_form = BikeDonationForm(request.POST or None)
  success_template = ''
  if bike_donation_form.is_valid():
    bike_donation = bike_donation_form.save(commit=False)
    bike_donation.geocode()
    bike_donation.date_input = date.today()
    bike_donation.save()
    success_header = gettext('website_bikedonation_success_header')
    success_text = gettext('website_bikedonation_success_message')
    success_context = {
      'success_header': success_header,
      'success_text': success_text,
    }
    return render(request,'website/form_success.html',success_context)

  context = {
      'bike_donation_form': bike_donation_form,
  }
  return render(request, 'website/bike_donation.html', context)

def website_supportingmember(request):
  template = 'website/supporting_member.html'
  success_template = 'website/form_success.html'

  print (request)
  if (request.method == "POST"):
    name = request.POST['inputName']
    surname = request.POST['inputSurname']
    street = request.POST['inputStreet']
    postal_code = request.POST['inputZip']
    city = request.POST['inputCity']
    mail = request.POST['inputMail']
    phone = request.POST['inputPhone']
    newsletter = True if request.POST['inputNewsletter']=="on" else False
    supportOption = request.POST['supportOptions']
    supportVariousAmount = request.POST['inputSupportVariousAmount']
    iban = request.POST['inputIban']
    bic = request.POST['inputBic']
    sepa = True if request.POST['inputMandat']=="on" else False

    amount = supportVariousAmount if supportOption == "other" else supportOption

    supporting_member = SupportingMember(
      name = name,
      surname = surname,
      street = street,
      postal_code = postal_code,
      city = city,
      mail = mail,
      phone = phone,
      newsletter = newsletter,
      amount = amount,
      iban = iban,
      bic = bic,
      sepa = sepa,
      date_signup = date.today()
      )

    supporting_member.save()

    #TODO: Maybe send a mail directly to the supportingmember

    success_header = gettext('website_supportingmember_success_header')
    success_text = gettext('website_supportingmember_success_message')
    success_context = {
      'success_header': success_header,
      'success_text': success_text,
    }
    return render(request, success_template, success_context)

  return render(request,template)


