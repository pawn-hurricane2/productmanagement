from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)