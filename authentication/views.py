from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, CreateGroupForm, getGroupGivenIDEndings
from django.core.mail import send_mail
from django.conf import settings


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
                    return redirect('main')
                else:
                    return redirect('home')
                
    return render(request, 'signin.html')

def SignUp(request):
    if request.user.is_authenticated:
        messages.error(request, "You can't sign up because you already are. To do this please sign out.")
        return redirect('main')
    
    signUp_form = SignUpForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and signUp_form.is_valid():
        # emailAdress = signUp_form.cleaned_data['email']
        # first_name = signUp_form.cleaned_data['firstname']
        # last_name = signUp_form.cleaned_data['lastname']


        signUp_form.save()
        messages.success(request, "Account successfully created.")

        #send_mail(
            #"Thank you for joining TaskSphere",
            #f"Hello, {first_name} {last_name}. \n We are pleased that you have chosen TaskSphere. If any problems arise over time, please contact our support. We wish you a lot of fun and good luck working with Tasksphere!",
            #settings.EMAIL_HOST_USER,
            #[emailAdress],
            #fail_silently=False,
        #)

        return redirect('signin')
    
    return render(request, 'signup.html', {'signUp_form': signUp_form,})


def ChooseGroupAction(request):
    if request.user.is_authenticated:
        if request.user.group is not None:
            messages.error(request, "You are already part of a group. Please leave the group first.")
            return redirect('main')
        else:
            return render(request, 'chooseGroupAction.html', {'username':request.user.firstname})
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('signin')

def CreateGroup(request):
    if request.user.is_authenticated:
        if request.user.group is not None:
            messages.error(request, "You are already part of a group. Please leave the group first.")
            return redirect('main')
        else:
            createGroup_form = CreateGroupForm(request.POST or None)
            if request.method == 'POST' and createGroup_form.is_valid():
                givenID = createGroup_form.cleaned_data['givenID']
                createGroup_form.save()
                group = Group.objects.get(givenID=givenID)
                request.user.group = group
                request.user.save()
                messages.success(request, "Group successfully created.")
                return redirect('main')
            return render(request, 'createGroup.html', {'createGroup_form': createGroup_form,})
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('signin')

def JoinGroup(request):
    if request.user.is_authenticated:
        if request.user.group is not None:
            messages.error(request, "You already are part of a group. Please leave the group first.")
            return redirect('main')
        else:
            if request.method == 'POST':
                group_id = request.POST['groupIDInput'] + request.POST['groupIDEndingInput']
                group_password = request.POST['groupPasswordInput']

                group_exists = Group.objects.filter(givenID=group_id).exists()
                
                if not group_exists or not Group.objects.get(givenID=group_id).group_password == group_password:
                    messages.error(request, "You entered the wrong group id or password") 
                    return render(request, 'joingroup.html', {'groupIDEnding': getGroupGivenIDEndings(), 'selected_value': request.POST['groupIDEndingInput'], 'group_id': request.POST['groupIDInput']})
                else:
                    group = Group.objects.get(givenID=group_id)
                    request.user.group = group
                    request.user.save()
                    messages.success(request, f"You entered the group {group.group_name}.")
                    return redirect('main')
                    
            return render(request, 'joingroup.html', {'groupIDEnding': getGroupGivenIDEndings()})
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('signin')
    
def LeaveGroup(request):
    if request.user.is_authenticated:
        if request.user.group is None:
            messages.error(request, "You are not part of a group.")
            return redirect('main')
        else:
            user_group = request.user.group.group_name
            request.user.group = None
            request.user.save()
            messages.success(request, f'You left the group "{user_group}" successfully.')

            return redirect('main')
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('signin')

def DeleteAccount(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            passwordPOST = request.POST['passwordPOST']
            user = authenticate(request, email=request.user.email, password=passwordPOST)

            if user is not None:
                if request.user.group is not None:
                    request.user.group == None
                logout(request)
                User.objects.get(email = user.email).delete()
                # -----------------Send user email to confirm the deletion of the account--------------------------
                messages.success(request, "Deleted your account successfully. We hope to see you again soon!")
                return redirect("main")
            else:
                messages.error(request, "You have entered the wrong password.")
                return redirect('deleteaccount')
        return render(request, 'deleteAccount.html')
    else:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('signin')

def SignOut(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('signin')