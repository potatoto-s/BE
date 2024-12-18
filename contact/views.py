from django.shortcuts import render, redirect
from .services import save_and_send_inquiry
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            save_and_send_inquiry(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                message=form.cleaned_data['message'],
                company_name=form.cleaned_data['company_name'],
                prefered_reply=form.cleaned_data['prefered_reply']
            )
            return redirect('success_page')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
