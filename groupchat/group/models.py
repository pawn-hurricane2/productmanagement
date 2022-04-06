from datetime import datetime

from django.db import models

# Create your models here.


class RegisteredUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=datetime.now)
    modified_date = models.DateTimeField(default=datetime.now)
    cell_phone = models.IntegerField()
    last_login = models.DateTimeField(default=datetime.now)

    @property
    def is_authenticated(self):
        return True


class Group(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    admin_user_id = models.IntegerField()
    creation_date = models.DateTimeField(default=datetime.now)


class Message(models.Model):
    content = models.CharField(max_length=500)
    user_id = models.IntegerField()
    creation_date = models.DateTimeField(default=datetime.now)
    group_id = models.IntegerField()


class GroupUsers(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()