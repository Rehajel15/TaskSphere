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
        return redirect("main")
    else:
        if request.method == 'POST':
            email = request.POST['emailInput']
            password = request.POST['passwordInput']

            if len(email) > 30:
                messages.error(request, 'The entered email address is too long.')
                return render(request, 'signin.html',)

            user = authenticate(request, email=email, password=password)

            if user is None:
                messages.error(request, "Wrong email or password. Please try again.")
                return redirect('signin')
            else:
                login(request, user)
                if user.group is None:  # in_group is empty
                    return redirect('/authentication/signup/choosegroupaction')
                else:
                    return redirect('home')
                
    return render(request, 'signin.html')

def SignUp(request):
    if request.user.is_authenticated:
        messages.error(request, "You can't sign up because you already are. To do this please sign out.")
        return redirect('main')
    
    signUp_form = SignUpForm()

    if request.method == 'POST':
        signUp_form = SignUpForm(request.POST or None, request.FILES or None)
        if signUp_form.is_valid():
            signUp_form.save()
            messages.success(request, "Account created successfully.")
            return redirect('main')
    
    return render(request, 'signup.html', {'signUp_form': signUp_form,})


def ChooseGroupAction(request):
    if request.user.is_authenticated:
        if request.user.in_group is not None:
            messages.error(request, "You already part of a group. Please leave the group first.")
            return redirect('main')
        else:
            return render(request, 'chooseGroupAction.html')
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('signin')

def JoinGroup(request):
    if request.user.is_authenticated:
        if request.user.in_group is not None:
            messages.error(request, "You already part of a group. Please leave the group first.")
            return redirect('main')
        else:
            return render(request, 'joingroup.html')
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('signin')

def SignOut(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('signin')