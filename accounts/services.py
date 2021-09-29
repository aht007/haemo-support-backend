from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from haemosupport.settings import DEFAULT_FROM_EMAIL

from .utils import password_reset_token


class MailService:
    """
    Mail service for sending mail to new user' email
    """
    @staticmethod
    def send_email_for_password_creation(request, user):
        """
        Function to send mail to new user for password creation
        """
        recepient_email = user.email
        subject = "Password Creation Alert"
        sender = DEFAULT_FROM_EMAIL
        site = get_current_site(request)  # for the domain
        html_content = render_to_string(
            'accounts/create_password.html', {
                'user': user.username,
                'protocol': 'http',
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': password_reset_token.make_token(user),
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
