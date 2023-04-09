from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from django.http import HttpResponse
from .models import Comment, Category, Content, Message, School
from .forms import ContentForm, UserForm, MyUserCreationForm, ContactForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json, requests
# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong Username OR password')

    context={'page':page}
    return render(request, 'home/login_registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')
    # return redirect('home/login_registration.html')

def registerUser(request):
    form = MyUserCreationForm()
    schools = School.objects.all()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured')

    return render(request, 'home/login_registration.html', {'form': form, 'schools':schools})


@login_required(login_url='/login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # rooms = Room.objects.filter(category__name__icontains=q, school_name_icontains= !!user's School !! ) 
    # rooms = Room.objects.filter(Q(category__name__icontains=q) & Q(name_icontans=q)) 
    contents = Content.objects.filter(Q(category__name__icontains=q) | Q(name__icontains=q)| Q(description__icontains=q))
    
    categories = Category.objects.all()
    
    # room_messages need to be replaced as room body, so Message -> Room.objects.get(something)
    content_comments = Comment.objects.filter(Q(content__category__name__icontains=q))

    context = {'contents': contents, 'categories': categories, 'content_comments': content_comments}
    return render(request, 'home/home.html', context)

@login_required(login_url='/login')
def content(request, pk):
    content = Content.objects.get(id=pk)
    content_comments = content.comment_set.all()

    # content_schools = Content.objects.get(Content.school)

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            content=content,
            body = request.POST.get('body')
        )
        
        return redirect('content', pk=content.id)
    context = {'content': content, 'content_comments':content_comments}
    return render(request, 'home/content.html', context)

@login_required(login_url='/login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    contents = user.content_set.all()
    content_comments = user.comment_set.all()
    categories = Category.objects.all()
    context = {'user':user, 'contents': contents, 'content_comments': content_comments, 'categories': categories}
    return render(request, 'home/profile.html', context)




# @login_required need to be attached others
@login_required(login_url='/login')
def createContent(request):
    form = ContentForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, create = Category.objects.get_or_create(name=category_name)

        Content.objects.create(
            host=request.user,
            category=category,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'categories': categories}
    return render(request, 'home/content_form.html', context)
    

@login_required(login_url='/login')
def updateContent(request, pk):
    content = Content.objects.get(id=pk)
    form = ContentForm(instance=content)
    category = Category.objects.all()
    if request.user != content.host:
        return HttpResponse('You are not allowed to modify')

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, create = Category.objects.get_or_create(name=category_name)
        content.name = request.POST.get('name')
        content.category = category
        content.description = request.POST.get('description')
        content.save()
        return redirect('home')

    context={'form': form, 'category': category, 'content':content}
    return render(request, 'home/content_form.html', context)

@login_required(login_url='/login')
def deleteContent(request, pk):
    content = Content.objects.get(id=pk)

    if request.user != content.host:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        content.delete()
        return redirect('home')
    return render(request, 'home/delete.html', {'obj':content})


@login_required(login_url='/login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'home/delete.html', {'obj':comment})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    contents = Content.objects.all()

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'home/update-user.html', {'form': form, 'contents': contents})


@login_required(login_url='/login')
def userMessage(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            phone = form.cleaned_data['phone']
            Message.objects.create( name=name, email=email, phone=phone, message=message)
        return redirect('home')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'home/contact.html', context)


