from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.models import User
from django.contrib import messages


def homepage(request):
    products = Product.objects.all()
    return render(request, 'home_page.html', {'products': products})

def login_view(request):
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        user = User.objects.create_user(username=email, email=email, password=pass1)
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number

        print(user.phone_number)

        user.save()

        messages.success(request, 'Tavs profils tika reģistrēts')
        return redirect('login')
    return render(request, 'register.html')