from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import default_storage

class socialmedia(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uname = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    pass1 = models.CharField(max_length=100)
    pass2 = models.CharField(max_length=100)
    profilepicture = models.ImageField(upload_to='media/',blank=True)
    bio=models.CharField(max_length=200,default=True)
    title = models.CharField(max_length=100,default=True)
    content = models.CharField(max_length=100,default=True)
    post = models.ImageField(upload_to='media/',blank=True)
    
    def save(self, *args, **kwargs):
        try:
            old_obj = socialmedia.objects.get(id=self.id)
            if old_obj.profilepicture and old_obj.profilepicture != self.profilepicture:
                default_storage.delete(old_obj.profilepicture.path)
        except socialmedia.DoesNotExist:
            pass

        super().save(*args, **kwargs)


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
