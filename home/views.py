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

        task_filter = {
            'ToDo': [],
            'In_progress': [],
            'Done': []
        }

        for task in request.user.group.table.tasks.all():
            if task.current_column == 'ToDo':
                task_filter['ToDo'].append(task)
            elif task.current_column == 'In progress':
                task_filter['In_progress'].append(task)
            else: 
                task_filter['Done'].append(task)
            

        return render(request, 'home/main.html', {"task_filter":task_filter})
    
def employees_page(request):
    if not request.user.is_authenticated:
        messages.error(request, "To have access to this page you need to sign in.")
        return redirect('authentication:signin')
    elif request.user.group is None:
        messages.error(request, "To have access to this page you need to be part of a group.")
        return redirect('authentication:choosegroupaction')
    else:
        # Assuming the user has a group and the group has a table
        employees = request.user.group.users
        return render(request, 'home/employees.html', {'employees': employees})