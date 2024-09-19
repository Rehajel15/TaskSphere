from django.shortcuts import render, redirect
from authentication.models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm


# Create your views here.

def main(request):
    return render(request, 'main.html')

def SignIn(request):
    if request.user.is_authenticated:
        messages.error(request, f"You can't sign in because you already are. To do this please sign out.")
        return redirect('/authentication/')
    else:
        if request.method == 'POST':
            email = request.POST['emailInput']
            password = request.POST['passwordInput']
            errorType = None

            if len(email) > 30:
                messages.error(request, 'The entered email address is too long.')
                errorType = 'emailTooLong'
                return render(request, 'signin.html', {'errorType': errorType, 'password': password})
            
            if len(password) > 100:
                messages.error(request, 'The entered password is too long.')
                errorType = 'passwordTooLong'
                return render(request, 'signin.html', {'errorType': errorType, 'email': email})
            

            user = authenticate(request, email=email, password=password)

            if user is None:
                messages.error(request, "Wrong email or password. Please try again.")
                return redirect('/authentication/signin/')
            else:
                login(request, user)
                if user.in_group is None:  # in_group is empty
                    return redirect('/authentication/signup/choosegroupaction')
                else:
                    return redirect('/home')
                
    return render(request, 'signin.html')

def SignUp(request):
    if request.user.is_authenticated:
        messages.error(request, "You can't sign up because you already are. To do this please sign out.")
        return redirect('/authentication/')
    
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('/authentication')
    
    return render(request, 'signup.html', {'form': form})


def ChooseGroupAction(request):
    if request.user.is_authenticated:
        if request.user.in_group is not None:
            messages.error(request, "You already part of a group. Please leave the group first.")
            return redirect('/authentication/')
        else:
            return render(request, 'chooseGroupAction.html')
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('/authentication/signin/')

def JoinGroup(request):
    if request.user.is_authenticated:
        if request.user.in_group is not None:
            messages.error(request, "You already part of a group. Please leave the group first.")
            return redirect('/authentication/')
        else:
            return render(request, 'joingroup.html')
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('/authentication/signin/')

def SignOut(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('/authentication/signin/')