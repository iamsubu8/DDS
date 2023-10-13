from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Folder(models.Model):
    name = models.CharField(max_length=255,blank=True)
    file=models.ImageField(upload_to='file/',null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
