from django.db import models
from django.conf import settings

# Create your models here.

class ContactInquiries(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20)
    message = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=100, null=True)
    prefered_reply = models.CharField(max_length=100, null=False, blank=False)