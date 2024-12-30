from django.urls import path

from . import views

app_name = "contact"

urlpatterns = [
    path("inquiry", views.ContactInquiryView.as_view(), name="inquiry"),
    path("inquiry/success", views.ContactSuccessView.as_view(), name="inquiry-success"),
]
