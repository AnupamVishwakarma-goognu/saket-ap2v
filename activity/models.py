from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from anquira_v2 import choices

# Create your models here.
class Activity(models.Model):
    """
    user:
    action:
    action_ref_id:
    added_on:


    ACTIONS = (
        ('add_enquiry', 'Add Enquiry'),
        ('mod_enquiry', 'Modify Enquiry'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    )

    ACTION_DETAILS = (
        ('add_enquiry', 'The enquiry %d has been added.'),
        ('login', 'The user has been login.'),
    )

    Add Enquiry, The enquiry 10 has been added.

    ACTION_URL_MAPPING = (
        ('add_enquiry', 'enquiry_view(%d)'), # /enquiries/view/8480/
        ('add_followup', 'get_enquiry_by_followup(%d)'), # /enquiries/view/8480/
    )
    """

    user = models.ForeignKey('users.CustomUserModel', on_delete=models.SET_NULL, null=True, default=True)
    typee = models.CharField(max_length=255, null=True,blank=True)
    ref_type = models.CharField(max_length=255, null=True,blank=True)
    ref_id = models.CharField(max_length=255, null=True,blank=True)
    add_on = models.DateTimeField(auto_now_add=True)
    # action_url = models.CharField(max_length=10, null=True,blank=True)

    def type(self):
        return choices.Action.ACTIONS[self.typee]
    
    def action_details(self):
        # print("------")
        display_string = choices.ActionDetails.ACTION_DETAILS[self.typee]
        record_id = self.ref_id
        # print(self.typee)
        final_display_string = display_string.replace('%d',str(record_id))
        return final_display_string

    def a_url(self):
        # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        action_url1 = choices.ActionDetailsUrl.ACTION_DETAILS_URL[self.typee]
        # print(action_url1)
        record_id = self.ref_id
        action_url1 = action_url1.replace('id',str(record_id))
        return action_url1