
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anquira_v2.settings")
django.setup()

import datetime
from enquiries.models import Enquiries
from users.models import CustomUserModel as User

date_before =  datetime.datetime(2021, 8, 10)
exclude_owner = ["Kirti Tomer"] #kirti

# mobile number
id_skip = ["9711680701", "7053702652", "9501364950", "8837514579", "9560177978", "7017001983", "8770443240", "8553585927", "7903467820", "9015907765", "7504178766", "8295622378", "7011228573", "9752973233", "9893037177", "9711597623", "9582402956", "9971124233"]        #skip enquires id in this list.

enq_obj = Enquiries.objects.filter(added_on__lte = date_before).exclude(reference="Marketing Agency").exclude(assigned_by__first_name__in=exclude_owner).exclude(mobile__in=id_skip)
print("Total:", enq_obj.count())

n = 1
new_owner_id = [4,22]

for i in enq_obj:
    print(n)
    if n%2==0:
        Enquiries.objects.filter(id=i.id).update(
            assigned_by=User.objects.get(id=new_owner_id[0])
        )
    else:
        Enquiries.objects.filter(id=i.id).update(
            assigned_by=User.objects.get(id=new_owner_id[1])
        )
    n=n+1

Enquiries.objects.filter(mobile__in=id_skip).update(
            assigned_by=User.objects.get(id=new_owner_id[1])
        )
