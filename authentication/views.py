from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def main(request):
    return render(request, 'main.html')

def SignIn(request):
    if request.user.is_authenticated:
        messages.error(request, f"You can't sign in because you already are. To do this please sign out.")
        return redirect('/authentication/')
    else:
        if request.method == 'POST':
            email = request.POST.get('emailInput')
            password = request.POST.get('passwordInput')

            try:
                username = User.objects.get(email=email).username
            except User.DoesNotExist or user is None:
                messages.error(request, "Wrong email or password. Please try again.")
                return redirect('/authentication/signin/')
            
            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, "Wrong email or password. Please try again.")
                return redirect('/authentication/signin/')
            else:
                login(request, user)
                return redirect('/authentication/home')
                
    return render(request, 'signin.html')

def SignUp(request):
    return render(request, 'signup.html')

def SignOut(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('/authentication/signin/')