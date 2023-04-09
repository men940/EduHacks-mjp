from django.contrib import admin

# Register your models here.
from .models import Content, Category, Comment, User, School, Message

admin.site.register(User)
admin.site.register(Content)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(School)
admin.site.register(Message)