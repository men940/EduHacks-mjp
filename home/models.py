from django.db import models
from django.contrib.auth.models import AbstractUser


class School(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Content(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    photo = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-create']

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-create']

    def __str__(self):
        return self.body[0:50] 
    

class Message(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=20, null=True)
    message = models.TextField(max_length=500, null=True)
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-create']
    