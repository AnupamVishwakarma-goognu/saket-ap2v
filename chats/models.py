import os
from django.db import models

# Create your models here.
class ChatFile(models.Model):
    batch = models.CharField(max_length=10, null=True, blank=True, default=None)
    file = models.FileField(upload_to="chat_files")
    current_batch_id_forward = models.CharField(max_length=10, null=True, blank=True, default=None)

    # def save(self):
    #     print("Calling Send SMS Function")
    #     # super(ChatFile, self).save()
    #     print(self.batch)
    #     print(self.file)

    #     path = '/media/documents/'
   
    #     # Check whether the specified
    #     # path exists or not
    #     isExist = os.path.exists(path)
    #     print(isExist)