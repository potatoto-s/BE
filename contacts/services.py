import logging
from typing import Any, Dict

from django.conf import settings
from django.core.mail import send_mail

from .models import Inquiry

logger = logging.getLogger(__name__)


class InquiryService:
    @staticmethod
    def create_inquiry(data: Dict[str, Any]) -> Inquiry:
        inquiry = Inquiry.objects.create(**data)

        try:
            subject = f"[HandsLive] 새로운 문의가 접수되었습니다. (문의번호: {inquiry.id})"
            message = f"""
            문의 내용:
            
            이름: {inquiry.name}
            이메일: {inquiry.email}
            전화번호: {inquiry.phone}
            문의 유형: {'기업' if inquiry.inquiry_type == 'COMPANY' else '공방'}
            {inquiry.inquiry_type == 'COMPANY' and '기업명' or '공방명'}: {inquiry.organization_name}
            선호 연락 방법: {'이메일' if inquiry.preferred_contact == 'EMAIL' else '전화'}
            
            문의 내용:
            {inquiry.content}   
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,  # jungseungwon0113@gmail.com
                recipient_list=[settings.EMAIL_HOST_USER],  # 같은 이메일로 받기
                fail_silently=False,
            )

            logger.info(f"이메일 발송 성공: 문의번호 {inquiry.id}")

        except Exception as e:
            logger.error(f"이메일 발송 실패: {str(e)}")
            # 이메일 발송 실패해도 문의는 저장됨

        return inquiry
