from django.conf import settings
from django.core.mail import send_mail

from .models import ContactInquiries


def save_and_send_inquiry(name, email, phone, message, company_name, prefered_reply):
    inquiry = ContactInquiries.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message,
        company_name=company_name,
        prefered_reply=prefered_reply,
    )

    email_subject = f"새로운 문의가 접수되었습니다 - {name}"
    email_message = f"""
    새로운 문의가 접수되었습니다.
    
    이름: {name}
    이메일: {email}
    전화번호: {phone}
    회사명: {company_name}
    선호하는 답변 방식: {prefered_reply}
    
    문의 내용:
    {message}
    """

    send_mail(
        subject=email_subject,
        message=email_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )

    return inquiry
