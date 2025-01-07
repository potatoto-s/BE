from django.conf import settings
from django.db import models

# Create your models here.


class ContactInquiries(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20)
    # 기업인지 공방인지
    organizationName = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    inquiry_type = models.CharField(max_length=100, null=False)
    prefered_contact = models.CharField(max_length=100, null=False, blank=False)
