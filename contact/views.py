from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ContactInquirySerializer
from .services import save_and_send_inquiry


class ContactInquiryView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContactInquirySerializer(data=request.data)
        if serializer.is_valid():
            inquiry = save_and_send_inquiry(**serializer.validated_data)
            return Response(
                ContactInquirySerializer(inquiry).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "문의가 성공적으로 접수되었습니다."})
