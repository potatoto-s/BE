from django import forms


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
