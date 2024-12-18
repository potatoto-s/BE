from rest_framework import serializers
from .models import ContactInquiries

class ContactInquirySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    message = serializers.CharField()
    company_name = serializers.CharField(max_length=100, allow_null=True)
    prefered_reply = serializers.ChoiceField(choices=['email', 'phone'])
    created_at = serializers.DateTimeField(read_only=True)

    def validate_prefered_reply(self, value):
        if value not in ['email', 'phone']:
            raise serializers.ValidationError("선호하는 답변 방식은 'email' 또는 'phone'이어야 합니다.")
        return value

    def create(self, validated_data):
        return ContactInquiries.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.message = validated_data.get('message', instance.message)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.prefered_reply = validated_data.get('prefered_reply', instance.prefered_reply)
        instance.save()
        return instance
