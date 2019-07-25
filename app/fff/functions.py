from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext

class EmailService():
  rw_email = "mail.rueckenwind@gmail.com"

  def send_email(self, template, context, to_email, subject, reply_to):
    email_text = render_to_string(template,context)
    email_message = EmailMessage(subject=subject, body=email_text, from_email = self.rw_email, to = to_email, reply_to = reply_to)
    email_message.content_subtype = "html"
    email_message.send()

  def send_contact_success(self, name, reply_to, phone, message):
    to_email = ['jakobschult@yahoo.de']
    reply_to_list = list()
    reply_to_list.append(reply_to)
    subject = gettext('Contact')
    template = 'emails/send_contact_success.html'
    context = {
    'name':name,
    'email':reply_to,
    'phone':phone,
    'message':message,
    }
    self.send_email(template = template, context = context, to_email=to_email, subject=subject, reply_to = reply_to_list)

  def send_order_saved(self,name, email):
    to_email = email
    reply_to_list = list()
    reply_to_list.append(self.rw_email)
    subject = gettext('We put you on our waiting list')
    template = 'emails/send_order_saved.html'
    context = {
    'name':name
    }
    self.send_email(template = template, context = context, to_email=to_email, subject=subject, reply_to = reply_to_list)

  def send_order_invited(self):
    pass

  def send_new_supporting_member_info(self,name, email):
    to = ['jakobschult@yahoo.de']
    subject = gettext ('New sponsoring member')

  def send_new_supporting_member_external(self,name, email):
    to = email
    subject = gettext ('New sponsoring member')
