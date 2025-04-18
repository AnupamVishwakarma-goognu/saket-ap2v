import uuid

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE, related_name='profile')
    last_visit = models.DateTimeField()


# This model is used to give date and time when a message was created/modified.
class DateTimeModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Room(DateTimeModel):
    id = models.UUIDField(primary_key=True,
            default=uuid.uuid4,
            editable=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        memberset = self.members.all()
        members_list = []
        for member in memberset:
            members_list.append(member.first_name)

        return ", ".join(members_list)

    @property
    def last_message(self):
        lm = self.message_set.order_by('-id')

        if len(lm) > 0:
            return lm[0].sender, lm[0].text

        return "", "No message"


class Message(DateTimeModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='sender')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='recipients')
    file_id = models.IntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.text} sent by "{self.sender}" in Room "{self.room}"'

    class Meta:
        ordering = ['-id']
