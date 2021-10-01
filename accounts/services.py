"""
Mail Service Module for Accounts App
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from haemosupport.settings import DEFAULT_FROM_EMAIL


def send_mail_to_new_users(user_list, domain):
    """
    Function to iterate over user list and send mail
    """
    for user in user_list:
        send_email_for_password_creation(user, domain)


def send_email_for_password_creation(user, domain):
    """
    Function to send mail to new user for password creation
    """
    token_generator = PasswordResetTokenGenerator()
    recepient_email = user.email
    subject = "Password Creation Alert"
    sender = DEFAULT_FROM_EMAIL
    html_content = render_to_string(
        'accounts/create_password.html', {
            'user': user.username,
            'protocol': 'http',
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        })

    plain_text = strip_tags(html_content)
    send_mail(subject, plain_text,
              sender,
              [
                  recepient_email,
              ],
              html_message=html_content,
              fail_silently=False
              )
