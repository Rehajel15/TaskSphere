# models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid
from datetime import datetime
from django.core.validators import MaxValueValidator

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=30)
    givenID = models.CharField(max_length=40, unique=True)  # ID that can be changed
    group_password = models.CharField(max_length=30)
    group_biography = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), editable=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Hashes and sets the password for the group

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Checks the input of a user

    def __str__(self):
        return f"{self.group_name} || {self.givenID}"
    
    
class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.OneToOneField(Group, null=True, on_delete=models.CASCADE, editable=False) # Connect to Group
    
    def __str__(self):
        return str(self.id)
        

    
class Table_task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=30, unique=True)
    task_description = models.TextField(max_length=150, blank=True, null=True)
    current_column = models.CharField(max_length=15, blank=False, null=False, choices=[('ToDo', 'ToDo'), ('In progress', 'In progress'), ('Done', 'Done')])
    current_worker = models.CharField(max_length=30) 
    deadLine = models.DateTimeField()
    created_on = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), editable=False)
    table = models.ForeignKey(Table, related_name='tasks', on_delete=models.CASCADE)  # Connection with table

    def __str__(self):
        return f"Name: {self.task_name} || ID: {self.id} || Created on: {self.created_on} || Table: {self.table}"


