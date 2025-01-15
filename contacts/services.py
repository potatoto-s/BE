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
        InquiryService.send_inquiry_email(inquiry, is_update=False)
        return inquiry

    @staticmethod
    def update_inquiry(inquiry: Inquiry, data: Dict[str, Any]) -> Inquiry:
        # 수정 전 데이터 백업
        original_data = {
            "name": inquiry.name,
            "email": inquiry.email,
            "phone": inquiry.phone,
            "content": inquiry.content,
            "inquiry_type": inquiry.inquiry_type,
            "organization_name": inquiry.organization_name,
            "preferred_contact": inquiry.preferred_contact,
        }

        # 데이터 수정
        for key, value in data.items():
            setattr(inquiry, key, value)

        # 변경사항이 있는지 확인
        has_changes = any(getattr(inquiry, key) != original_data[key] for key in original_data)

        if has_changes:
            inquiry.save()
            # 이메일 발송
            InquiryService.send_inquiry_email(inquiry, is_update=True)
            logger.info(f"문의 {inquiry.id} 수정 완료 및 이메일 발송")
        else:
            logger.info(f"문의 {inquiry.id} 변경사항 없음")

        return inquiry

    @staticmethod
    def send_inquiry_email(inquiry: Inquiry, is_update: bool = False):
        try:
            action = "수정" if is_update else "접수"
            subject = f"[HandsLive] 문의가 {action}되었습니다. (문의번호: {inquiry.id})"
            message = f"""
            문의 {action} 내용:
            
            이름: {inquiry.name}
            이메일: {inquiry.email}
            전화번호: {inquiry.phone}
            문의 유형: {'회사' if inquiry.inquiry_type == 'COMPANY' else '공방'}
            {inquiry.inquiry_type == 'COMPANY' and '회사명' or '공방명'}: {inquiry.organization_name}
            선호 연락 방법: {'이메일' if inquiry.preferred_contact == 'EMAIL' else '전화'}
            
            문의 내용:
            {inquiry.content}
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            logger.info(f"이메일 발송 성공: 문의번호 {inquiry.id} ({action})")

        except Exception as e:
            logger.error(f"이메일 발송 실패: {str(e)}")
