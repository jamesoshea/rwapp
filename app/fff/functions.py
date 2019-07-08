from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext

class EmailService():
  rw_email = "mail.rueckenwind@gmail.com"

  def send_contact_success(self, name, reply_to, phone, message):
    to_email = ['jakobschult@yahoo.de']
    reply_to = list(reply_to)
    subject = gettext('contact_form_email_subject')
    template = 'emails/send_contact_success.html'
    context = {
    'name':name,
    'email':reply_to,
    'phone':phone,
    'message':message,
    }
    send_email(template, context, to_email, subject, reply_to)

  def send_order_saved(name, email):
    to_email = email
    reply_to = list(self.rw_email)
    subject = gettext('order_saved_email_subject')+'Du hast dich erfolgreich auf unserer Warteliste eingetragen.'
    template = 'emails/send_order_saved.html'
    context = {
    'name':name
    }
    send_email(template, context, to_email, subject, reply_to)

  def send_order_invited():
    pass

  def send_new_supporting_member_info(name, email):
    to = ['jakobschult@yahoo.de']
    subject = gettext ('supportingmember_form_email_subject')

  def send_new_supporting_member_external(name, email):
    to = email
    subject = gettext ('supportingmember_form_email_subject')

  def send_mail(template, context, to_email, subject, reply_to):
    email_text = render_to_string(template,context)
    email_message = EmailMessage(subject=subject, body=email_text, from_email = self.rw_email, to = to_email, reply_to = replay_to)
    email_message.send()
