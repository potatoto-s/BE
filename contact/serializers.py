from rest_framework import serializers

from .models import ContactInquiries


class ContactInquirySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    organization_name = serializers.CharField(max_length=100)
    content = serializers.CharField()
    inquiry_type = serializers.CharField(max_length=100)
    prefered_contact = serializers.ChoiceField(choices=["email", "phone"])
    created_at = serializers.DateTimeField(read_only=True)

    def validate_prefered_contact(self, value):
        if value not in ["email", "phone"]:
            raise serializers.ValidationError(
                "선호하는 답변 방식은 'email' 또는 'phone'이어야 합니다."
            )
        return value

    def create(self, validated_data):
        return ContactInquiries.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.content = validated_data.get("message", instance.content)
        instance.organization_name = validated_data.get(
            "organization_name", instance.organization_name
        )
        instance.inquiry_type = validated_data.get(
            "inquiry_type", instance.inquiry_type
        )
        instance.prefered_reply = validated_data.get(
            "prefered_contact", instance.prefered_contact
        )
        instance.save()
        return instance
