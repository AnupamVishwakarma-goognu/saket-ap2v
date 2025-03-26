from django.core.management.base import BaseCommand
from users.models import CustomUserModel

class Command(BaseCommand):
    help = 'username regenrate'
    def handle(self, *args, **kwargs):
        user_obj = CustomUserModel.objects.all()
        for i in user_obj:
            email = i.email
            print("Email : ", email)
            # a = email.split("@")
            b = email.replace("@",'.')
            # b = a[0]
            print('Username : ',b)

            CustomUserModel.objects.filter(id=i.id).update(
                username = b
            )
            print("Username is update for id : ", i.id)
            print("--------------------------------------------------")