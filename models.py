from django.db import models
from django.contrib.auth.models import User

# tasks/models.py


class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)  # 🗓️ New
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')  # 📌 New
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
  
# Create your models here.

