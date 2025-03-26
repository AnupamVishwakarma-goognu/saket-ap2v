from django.core.management.base import BaseCommand
import datetime
import random
from enrolls.models import Installments

class Command(BaseCommand):
    help = 'Change Default in installment__paid_on'

    def handle(self, *args, **kwargs):
        installment_obj = Installments.objects.filter(paid_on__isnull=True)

        for i in installment_obj:
            Installments.objects.filter(id=i.id).update(
                paid_on = i.due_date
            )
            print("Installment No: ",i.id," ,paid_on date changed to :",i.due_date)