from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username    
    


class Contacts(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contacts = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_contacts',blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.contacts.username}'
    
    
class ProfilePhoto(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile_photo')
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    
    def __str__(self):
        return self.user.username