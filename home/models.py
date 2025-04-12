# models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid
from datetime import datetime
from django.core.validators import MaxValueValidator

class GroupGivenIDEnding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ending = models.CharField(max_length=5)
    whole_name = models.CharField(max_length=40)

    def __str__(self):
        return str(f"{self.ending}")

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=30)
    givenID = models.CharField(max_length=40, unique=True)  # ID that can be changed
    givenID_ending = models.ForeignKey(GroupGivenIDEnding, related_name='Groups', on_delete=models.DO_NOTHING)
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
        

class Table_taskColumn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    column_name = models.CharField(max_length=30,)
    column_description = models.TextField(max_length=150, blank=True, null=True)
    column_color = models.CharField(max_length=5, blank=False, null=False)
    table = models.ForeignKey(Table, related_name='taskColumns', on_delete=models.CASCADE)  # Connection with table
    position = models.IntegerField(null=False, blank=False)  # Beginning from the right

    def __str__(self):
        return f"Name: {self.column_name} || ID: {self.id} || Table: {self.table}"
    
class Table_task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=30)
    task_description = models.TextField(max_length=150, blank=True, null=True)
    current_column = models.CharField(max_length=30)
    current_worker = models.CharField(max_length=30) 
    deadLine = models.DateTimeField()
    created_on = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), editable=False)
    table = models.ForeignKey(Table, related_name='tasks', on_delete=models.CASCADE)  # Connection with table

    def __str__(self):
        return f"Name: {self.task_name} || ID: {self.id} || Created on: {self.created_on} || Table: {self.table}"


