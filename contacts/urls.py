from django.urls import path

from .views import InquiryCreateView, InquiryDetailView

urlpatterns = [
    path("", InquiryCreateView.as_view(), name="inquiry-create"),
    path("<int:inquiry_id>/", InquiryDetailView.as_view(), name="inquiry-detail"),
]
