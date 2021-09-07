import requests
from donation.serializers import (BaseSerializer,
                                  DonationUserSerializer,
                                  DonationInProgressActionSerializer)
from donation.models import DonationRequest
from rest_framework import generics, permissions, parsers, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from python_http_client import exceptions
import sendgrid
from sendgrid.helpers.mail import (Mail,
                                   Email,
                                   Personalization
                                   )
from haemosupport.settings import (
    SENDGRID_API_KEY, DEFAULT_FROM_EMAIL,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
from django.db.models import signals
from django.dispatch import receiver
from twilio.rest import Client


class IsUserAuthorized(permissions.BasePermission):
    def has_object_permission(self, request, view, donation_obj):
        return (donation_obj.created_by.id == request.user.id
                or request.user.is_admin)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'  # items per page


class DonationView(generics.ListCreateAPIView):
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filterset_fields = ['search_slug']
    serializer_class = DonationUserSerializer
    ordering = ['time']
    ordering_fields = ['priority']

    def get_queryset(self):
        if(self.request.user.is_admin):
            queryset = DonationRequest.objects.filter(
                Q(is_approved=False) &
                Q(is_rejected=False) &
                Q(in_progress=False)
            )
            return queryset
        else:
            queryset = DonationRequest.objects.filter(
                ~Q(created_by=self.request.user) &
                Q(is_approved=True) &
                Q(in_progress=False)).order_by('-time')
        return queryset


class UserRequestsView(generics.ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = DonationUserSerializer

    def get_queryset(self):
        return DonationRequest.objects.filter(created_by=self.request.user)


class DonationUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsUserAuthorized,
    ]
    queryset = DonationRequest.objects.all()
    serializer_class = DonationUserSerializer


class DonationAdminActionsView(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAdminUser,
    ]
    serializer_class = BaseSerializer
    queryset = DonationRequest.objects.all()


class DonationInProgressActionView(generics.UpdateAPIView):
    serializer_class = DonationInProgressActionSerializer
    queryset = DonationRequest.objects.all()

    @staticmethod
    def send_mail(template_id, sender, recipient, data_dict):
        print('here')
        sendGridClient = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        mail = Mail()
        mail.template_id = template_id

        mail.from_email = Email(sender)
        personalization = Personalization()
        personalization.add_to(Email(recipient))
        personalization.dynamic_template_data = data_dict
        mail.add_personalization(personalization)

        try:
            response = sendGridClient.client.mail.send.post(
                request_body=mail.get())
            print(response)
        except exceptions.BadRequestsError as e:
            print("INSIDE")
            print(e.body)

    @staticmethod
    @receiver(signals.post_save, sender=DonationRequest)
    def donation_request_approve_observer(sender, instance, created, **kwrags):
        """
        This method will send an email to both donor and requestor
        when a donation request becomes in progress
        """
        if(created is False):
            print(instance)
            if(instance.in_progress is True and instance.is_complete is False):
                try:
                    DonationInProgressActionView.send_email_to_donor(instance)
                    DonationInProgressActionView.send_email_to_requestor(
                        instance)
                    DonationInProgressActionView.send_sms_to_requestor(
                        instance)
                    DonationInProgressActionView.send_sms_to_donor(instance)

                except requests.HTTPError as exception:
                    print(exception)

    @staticmethod
    def send_email_to_donor(data):
        recepient_email = data.donated_by.email
        subject = "Donation Request Update"

        body = {}
        body['username'] = data.donated_by.username
        body['donation_role'] = "Requestor"
        body['related_name'] = data.created_by.username
        body['phone_number'] = data.created_by.phone_number
        body['email'] = data.created_by.email
        body['blood_group'] = data.blood_group
        body['quantity'] = data.quantity
        body['priority'] = data.priority
        body['location'] = data.location

        template_id = "d-4f03429f3f1a4db5a1aa80c02e563004"
        sender = DEFAULT_FROM_EMAIL
        data_dict = {"subject": subject, "body": body}
        DonationInProgressActionView.send_mail(
            template_id, sender, recepient_email, data_dict)

    @staticmethod
    def send_email_to_requestor(data):
        recepient_email = data.created_by.email
        subject = "Donation Request Update"

        body = {}
        body['username'] = data.created_by.username
        body['donation_role'] = "Donor"
        body['related_name'] = data.donated_by.username
        body['phone_number'] = data.donated_by.phone_number
        body['email'] = data.donated_by.email
        body['blood_group'] = data.blood_group
        body['quantity'] = data.quantity
        body['priority'] = data.priority
        body['location'] = data.location

        template_id = "d-4f03429f3f1a4db5a1aa80c02e563004"
        sender = DEFAULT_FROM_EMAIL
        data_dict = {"subject": subject, "body": body}
        DonationInProgressActionView.send_mail(
            template_id, sender, recepient_email, data_dict)

    @staticmethod
    def send_sms_to_requestor(data):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        body = ("Donor {donor_name} having Phone Number{phone_number} has"
                " accepted your request and will be"
                " in contact with you soon".format(
                    donor_name=data.donated_by.username,
                    phone_number=data.donated_by.phone_number))
        client.messages.create(
            body=body,
            from_=+12248084101,
            to=data.created_by.phone_number
        )

    @staticmethod
    def send_sms_to_donor(data):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        body = ("Requestor {requestor_name} having Phone Number{phone_number}"
                " awaits a call from you".format(
                    requestor_name=data.created_by.username,
                    phone_number=data.created_by.phone_number))
        client.messages.create(
            body=body,
            from_=+12248084101,
            to=data.donated_by.phone_number
        )
