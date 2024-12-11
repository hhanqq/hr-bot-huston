from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[
        ('intern', 'Стажёр'),
        ('employee', 'Сотрудник'),
        ('hr_manager', 'HR-менеджер')
    ])
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.surname} {self.name} ({self.phone})"