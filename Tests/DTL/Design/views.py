from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
    return render(request, 'index.html', {'message': 'Greeting from Coderooz!', 'name': 'TuteDude'})

def add(request):
    if request.method == 'POST':
        num1 = request.POST.get('username', 0)
        num2 = request.POST.get('email', 0)
        num3 = request.POST.get('password', 0)
        
        return render(request, 'result.html', {'name': num1, 'email': num2, 'password': num3})
    return render(request, 'add.html', {'message': 'Please fill the form to register.'})