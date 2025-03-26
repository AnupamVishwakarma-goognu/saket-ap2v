from django.core.management.base import BaseCommand
from users.models import CustomUserModel
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Create User Easily"

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', type=str, help="User Name", required=True)
        parser.add_argument('-e', '--email', type=str, help="Email Address", required=True)
        parser.add_argument('-p', '--password', type=str, help="Password", required=True)

    def handle(self, *args, **options):
        username = options.get('user')
        email = options.get('email')
        password = options.get('password')

        obj, created = CustomUserModel.objects.get_or_create(
            username = username,
            email = email
        )
        # make_password_var = make_password(password)
        obj.set_password(password)
        obj.save()
        if created:
            print('Your user is created now please login now.')
        else:
            print('This user is already created please check.')
