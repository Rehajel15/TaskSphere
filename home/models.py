from django.db import models
import uuid
from datetime import datetime

class Table_taskColumn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    column_name = models.CharField(max_length=30)
    column_description = models.CharField(max_length=150)
    column_color = models.CharField(max_length=10)

    def __str__(self):
        return str(self.column_name) + ' || ' + str(self.id)
    
class Table_task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=30)
    task_description = models.CharField(max_length=150)
    current_column = models.CharField(max_length=30)
    current_worker = models.CharField(max_length=30)
    deadLine = models.DateTimeField()
    created_on = models.DateTimeField(default=datetime.now, editable=False)

    def __str__(self):
        return str(self.task_name) + ' || ' + str(self.id)

class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_column = models.ForeignKey(Table_taskColumn, related_name='Table_taskColumn', on_delete=models.CASCADE)
    task = models.ForeignKey(Table_task, related_name='Table_task', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)

# Create your models here.
class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    givenID = models.CharField(max_length=40)
    group_name = models.CharField(max_length=30)
    group_description = models.CharField(max_length=150)
    created_on = models.DateTimeField(default=datetime.now, editable=False)
    data = models.ForeignKey(Table, related_name='data_tables', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.column_name) + ' || ' + str(self.givenID)