from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profil(models.Model):
    typecompte = (
        ('LM Manager','lm manager'),
        ('LM Engineer','lm engineer'),
        ('Quality Manager','quality manager'),
        ('Assistant Engineer','assistant engineer'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="users_profils/",null=True,blank=True)
    bio = models.TextField(null=True)
    licensenumber = models.CharField(max_length=300,null=True)
    dateofbirth = models.DateField(null=True)
    placeofbirth = models.CharField(max_length=300,null=True)
    address = models.CharField(max_length=300,null=True)
    profile = models.CharField(max_length=18,choices=typecompte)

    def __str__(self):
        return self.user.username
    