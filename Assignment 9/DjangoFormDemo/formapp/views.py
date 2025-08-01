from django.shortcuts import render, redirect
from .forms import ContactForm

def home_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Normally save to DB or send email
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'formapp/home.html', {'form': form})

def success_view(request):
    return render(request, 'formapp/success.html')
