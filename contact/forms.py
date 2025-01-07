from django import forms
from django.core.exceptions import ValidationError
import re

class HyphenPhoneNumber(forms.Form):
    def __call__(self, value):
        if '-' not in value:
            raise ValidationError('전화번호에 ')

class HyphenPhoneNumberValidator:
    def __call__(self, value):
        # 하이픈 포함 여부 검증
        if '-' not in value:
            raise ValidationError('전화번호에 하이픈(-)이 포함되어야 합니다.')
        # 유효한 형식 검증 (010-1234-5678)
        if not re.match(r'^\d{3}-\d{3,4}-\d{4}$', value):
            raise ValidationError('유효한 전화번호 형식이 아닙니다. 예: 010-1234-5678')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    content = forms.CharField(widget=forms.Textarea)
    organization_name = forms.CharField(max_length=100)
    inquiry_type = forms.CharField(
        choices=[
            ("company", "기업"),
            ("workshop", "공방")
        ]
    )
    prefered_contact = forms.ChoiceField(
        choices=[
            ("email", "이메일"),
            ("phone", "전화"),
        ]
    )
