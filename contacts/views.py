from django.shortcuts import render
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Inquiry
from .serializers import InquirySerializer
from .services import InquiryService


class InquiryCreateView(APIView):
    @extend_schema(
        request=InquirySerializer,
        responses={201: InquirySerializer},
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "name": "홍길동",
                    "email": "test@test.com",
                    "phone": "010-1234-5678",
                    "content": "문의 내용입니다.",
                    "inquiry_type": "COMPANY",  # COMPANY 또는 WORKSHOP
                    "organization_name": "테스트 회사",  # 회사명 또는 공방명
                    "preferred_contact": "EMAIL",  # EMAIL 또는 PHONE
                },
                request_only=True,
                summary="문의하기 예시",
            )
        ],
    )
    def post(self, request):
        serializer = InquirySerializer(data=request.data)
        if serializer.is_valid():
            inquiry = InquiryService.create_inquiry(serializer.validated_data)
            return Response(InquirySerializer(inquiry).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InquiryDetailView(APIView):
    def get(self, request, inquiry_id):
        try:
            inquiry = Inquiry.objects.get(id=inquiry_id)
            return Response(InquirySerializer(inquiry).data)
        except Inquiry.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=InquirySerializer,
        responses={200: InquirySerializer},
        description="문의 내용을 수정합니다.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "name": "홍길동",
                    "email": "test@test.com",
                    "content": "수정된 문의 내용입니다.",
                    "inquiry_type": "COMPANY",
                    "organization_name": "테스트 회사",
                    "preferred_contact": "EMAIL",
                },
            )
        ],
    )
    def patch(self, request, inquiry_id):
        try:
            inquiry = Inquiry.objects.get(id=inquiry_id)
            serializer = InquirySerializer(inquiry, data=request.data, partial=True)
            if serializer.is_valid():
                # update_inquiry 메서드를 통해 수정 및 이메일 발송
                updated_inquiry = InquiryService.update_inquiry(inquiry, serializer.validated_data)
                return Response(InquirySerializer(updated_inquiry).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Inquiry.DoesNotExist:
            return Response(
                {"detail": "문의를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"문의 수정 중 오류 발생: {str(e)}")
            return Response(
                {"detail": "문의 수정 중 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
