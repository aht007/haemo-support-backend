from django.core.management.base import BaseCommand
from accounts.models import BloodGroupTypes, MY_USER
import factory
import factory.django

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MY_USER
    email = factory.Faker('email')
    username = factory.Faker('name')
    password = factory.Faker('password')
    date_of_birth = factory.Faker('date_of_birth')
    phone_number = factory.Faker('phone_number')
    blood_group = factory.Iterator(BloodGroupTypes.choices)
    

class Command(BaseCommand):
    help = 'Seeds the Database'
    
    def add_arguments(self, parser):
        parser.add_argument('--users',
            default=1,
            type=int,
            help='The number of users to create.')

    def handle(self, *args, **options):
        for _ in range(options['users']):
            UserFactory.create()