from django.shortcuts import render, redirect
from authentication.models import CustomUser
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
            
            user = authenticate(username=email, password=password)

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
        messages.error(request, f"You can't sign in because you already are. To do this please sign out.")
        return redirect('/authentication/')
    else:
        if request.method == 'POST':
            post = {
                'emailInput': request.POST.get('emailInput'),
                'passwordInput': request.POST.get('passwordInput'),
                'passwordInput2': request.POST.get('passwordInput2'),
                'firstnameInput': request.POST.get('firstnameInput'),
                'lastnameInput': request.POST.get('lastnameInput'),
                'biographyInput': request.POST.get('biographyInput'),
                'profilePictureInput': request.FILES.get('profilePictureInput')
            }

            if not post['passwordInput'] == post['passwordInput2']:
                messages.error(request, "You repeated the wrong password. Please try again.")
                post_data = {key: value for key, value in post.items() if key != 'passwordInput2'}
                return render(request, 'signup.html', {'profile': post_data})
            
            else:
                new_user = CustomUser.objects.create(
                    email = post['emailInput'],
                    password = post['passwordInput'],
                    firstname = post['firstnameInput'], 
                    lastname = post['lastnameInput'],
                    biography = post['biographyInput'],
                    profile_picture = post['profilePictureInput'],
                )
                new_user.save()
                messages.success(request, "Account created successfully.")
                return redirect('/authentication/signin/')   
        return render(request, 'signup.html')

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