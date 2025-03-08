
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Stand model
class Stand(models.Model):
    stand_number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Stand {self.stand_number} - {self.location}"
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

# Application model
class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending"
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.stand.stand_number}"

# Title Deed Request model
class TitleDeedRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=[("Pending", "Pending"), ("Processed", "Processed")], default="Pending"
    )

    def __str__(self):
        return f"Title Deed - {self.user.username} - {self.stand.stand_number}"

    

