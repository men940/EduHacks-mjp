from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Content, User, Message

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'school']


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = '__all__'
        exclude = ['host']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['photo', 'name', 'username', 'email', 'bio', 'school']


class ContactForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'message']