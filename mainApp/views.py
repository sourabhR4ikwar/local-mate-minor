from django.shortcuts import render, redirect
from .models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def homePage(request):
    guides = { "guides" : [
        {"name":"sourabh","rate":800},
        {"name": "sachin", "rate": 700},
        {"name": "rishabh", "rate": 600},
    ]}
    reviews = { "reviews": [
        {"name": "sourabh", "message": "hello"},
        {"name": "sachin", "message": "world"},
        {"name": "rishabh", "message": "!"},
    ]}
    isLoggedIn = False
    username = request.session['username']
    if username != '':
        isLoggedIn = True

    return render(request,'homepage/homepage.html',context={
        "guides": guides,
        "reviews": reviews,
        "isLoggedIn": isLoggedIn,
        "details": {
            "username": username,
            "profile": request.session['image']
        }
    })

def loginPage(request):
    request.session['username'] = ''
    return render(request, 'auth/login.html')

def loginProcess(request):
    isLoggedIn = False
    username = ""
    password = ""
    if request.method == 'POST':
        isLoggedIn = True
        email = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            if user is not None and password == user.password :
                request.session['username'] = user.name
                request.session['image'] = user.profile
                return redirect('/')
        except User.DoesNotExist :
            request.session['username'] = 'User does not exist'
            return redirect('/')

    return redirect('/login')



def signUpPage(request):
    return render(request,'auth/signUp.html')


def signUpProcess(request):
    email = request.POST.get("email")
    password = request.POST.get("pass")
    name = request.POST.get("username")
    profile = request.FILES['profile']
    fs = FileSystemStorage()
    profileImage = fs.save(profile.name, profile)
    uploaded_img_url = fs.url(profileImage)
    p = User(email = email,password=password,name=name,profile=uploaded_img_url)  #blue wale fields models ki h
    p.save()

    return redirect('/')