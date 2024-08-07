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


        if CustomUser.objects.filter(email=post['emailInput']).exists():
            messages.error(request, "Account with this email address already exists.")
            post_data = {key: value for key, value in post.items() if key != 'emailInput'}
            post_data['errorType'] = 'emailExists'
            return render(request, 'signup.html', {'post': post_data})

        if len(post['emailInput']) > 30:
            messages.error(request, "Email address is too long.")
            post_data = {key: value for key, value in post.items() if key != 'emailInput'}
            post_data['errorType'] = 'emailAddressTooLong'
            return render(request, 'signup.html', {'post': post_data})
        
        if post['passwordInput'] != post['passwordInput2']:
            messages.error(request, "You repeated the wrong password. Please try again.")
            post_data = {key: value for key, value in post.items() if key != 'passwordInput2'}
            post_data['errorType'] = 'passwordUnequal'
            return render(request, 'signup.html', {'post': post_data})

        if len(post['passwordInput']) < 10 or not any(char.isalpha() for char in post['passwordInput']) or not any(char.isdigit() for char in post['passwordInput']):
            messages.error(request, "Password is too short or/and includes no numbers and letters.")
            post_data = {key: value for key, value in post.items() if key not in ['passwordInput', 'passwordInput2']}
            post_data['errorType'] = 'invalidPassword'
            return render(request, 'signup.html', {'post': post_data})
        
        if len(post['passwordInput']) > 100 :
            messages.error(request, "Sorry but your password is too long.")
            post_data = {key: value for key, value in post.items() if key not in ['passwordInput', 'passwordInput2']}
            post_data['errorType'] = 'passwordTooLong'
            return render(request, 'signup.html', {'post': post_data})
        
        if len(post['firstnameInput']) > 20 :
            messages.error(request, "Your firstname is too long. Try to shorten it.")
            post_data = {key: value for key, value in post.items() if key != 'firstnameInput'}
            post_data['errorType'] = 'firstnameTooLong'
            return render(request, 'signup.html', {'post': post_data})
        
        if len(post['lastnameInput']) > 20 :
            messages.error(request, "Your lastname is too long. Try to shorten it.")
            post_data = {key: value for key, value in post.items() if key != 'lastnameInput'}
            post_data['errorType'] = 'lastnameTooLong'
            return render(request, 'signup.html', {'post': post_data})
        
        if len(post['biographyInput']) > 150 :
            messages.error(request, "Your biography is too long. Maximum 150 characters!")
            post_data = {key: value for key, value in post.items() if key != 'biographyInput'}
            post_data['errorType'] = 'biographyTooLong'
            return render(request, 'signup.html', {'post': post_data})

        new_user = CustomUser.objects.create_user(
            email=post['emailInput'],
            password=post['passwordInput'],
            firstname=post['firstnameInput'],
            lastname=post['lastnameInput'],
            biography=post['biographyInput'],
            profile_picture=post['profilePictureInput']
        )
        new_user.save()
        messages.success(request, "Account created successfully.")
        return redirect('/')

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