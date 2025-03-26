from django.core.management.base import BaseCommand
from users.models import CustomUserModel

class Command(BaseCommand):
    help = "get user list from django model"

    def handle(self, *args, **options):
        print('These are all users')
        for user in CustomUserModel.objects.all():
            data = '''
            ----------------
            username = {0}
            email = {1}
            ----------------
            '''.format(user.username, user.email)
            print(data)
