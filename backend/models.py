from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField()
    sex = models.CharField(max_length=2)

    def __str__(self):
        return self.user.username
    
    
class Health(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Health')
    date = models.DateTimeField(auto_now_add=True)
    bmi = models.DecimalField(max_digits=6, decimal_places=4)  # For example, 123.4567
    weight = models.DecimalField(max_digits=7, decimal_places=2)  # For example, 1234.5678
    height = models.DecimalField(max_digits=6, decimal_places=2)  # For example, 123.4567


    def __str__(self):
        return f"Order {self.id} for {self.user.username}"
    
    
