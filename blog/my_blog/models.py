from django.db import models

# Create your models here.
from my_blog.choices import USER_ADMIN_CHOICES
from datetime import datetime


class Blog1(models.Model):
    text = models.TextField()
    user_id = models.IntegerField()
    like = models.IntegerField(default=0)


class Users1(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    cell_phone = models.CharField(max_length=10)
    is_admin = models.IntegerField(default=0, choices=USER_ADMIN_CHOICES)
    password = models.CharField(null=True , max_length=50)
    last_login = models.DateTimeField(default=datetime.now())
    liked_blog_id = models.IntegerField(default=0)

    @property
    def is_authenticated(self):
        return True