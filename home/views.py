from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def main(request):
    if not request.user.is_authenticated:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('authentication:signin')
    elif request.user.group is None:
        messages.error(request, "To have access to this page you need to be part of a group.")
        return redirect('authentication:choosegroupaction')
    else:
        # Assuming the user has a group and the group has a table
        group_table = request.user.group.table 
        return render(request, 'home/main.html', {"table":group_table})