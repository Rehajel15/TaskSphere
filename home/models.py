# models.py
from django.db import models
import uuid
from datetime import datetime

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    givenID = models.CharField(max_length=40)  # ID that can be changed
    group_name = models.CharField(max_length=30)
    group_password = models.CharField(max_length=30)
    group_description = models.CharField(max_length=150)
    created_on = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), editable=False)

    def __str__(self):
        return f"{self.group_name} || {self.givenID}"
    
class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, related_name='tables', on_delete=models.CASCADE)  # Conncetion to group
    
    def __str__(self):
        return str(self.id)

class Table_taskColumn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    column_name = models.CharField(max_length=30)
    column_description = models.CharField(max_length=150)
    column_color = models.CharField(max_length=10)
    table = models.ForeignKey(Table, related_name='taskColumns', on_delete=models.CASCADE)  # Connection with table
    position = models.IntegerField()  # Beginning from the right

    def __str__(self):
        return f"Name: {self.column_name} || ID: {self.id} || Table: {self.table}"
    
class Table_task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=30)
    task_description = models.CharField(max_length=150)
    current_column = models.CharField(max_length=30)
    current_worker = models.CharField(max_length=30) 
    deadLine = models.DateTimeField()
    created_on = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), editable=False)
    table = models.ForeignKey(Table, related_name='tasks', on_delete=models.CASCADE)  # Connection with table

    def __str__(self):
        return f"Name: {self.task_name} || ID: {self.id} || Created on: {self.created_on} || Table: {self.table}"


