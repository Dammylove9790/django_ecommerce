from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
USER_TYPE = (
    ('customer', 'customer'),
    ('vendor', 'vendor'),
)

class User(AbstractUser):
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
       if not self.username:
            email_username, _ = self.email.split('@')
            self.username = email_username
       super(User, self).save(*args, **kwargs) # Call the real save() method
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='images', default='default-user.jpg', blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    usertype = models.CharField(max_length=255, choices=USER_TYPE, default=None, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
       if not self.fullname:
           self.fullname = self.user.username
       super(Profile, self).save(*args, **kwargs) # Call the real save() method 
