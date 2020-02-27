from django.shortcuts import render, redirect
from .models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage



## ---------------------------------
##   Login / Signup / Forgot Password
## --------------------------------- 

def loginPage(request):
    error = None
    if 'error' in request.session:
        error = request.session['error']
        request.session['error'] = None

    return render(request, 'auth/login.html', context={
        "error": error
    })

def loginProcess(request):
    username = ""
    password = ""
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            if user is not None and password == user.password :
                request.session['userid'] = user.id
                request.session['username'] = user.name
                # request.session['image'] = user.profile
                return redirect('/')
            else:
                request.session['error'] = 'Invalid Username or Password'

        except User.DoesNotExist :
            request.session['error'] = 'User does not exist'

    return redirect('/login')



def signUpPage(request):
    isGuide = request.GET.get('q',False)
    # if isGuide != False:
    #     isGuide = True

    error = None
    if 'error' in request.session:
        error = request.session['error']
        request.session['error'] = None
    
    return render(request,'auth/signUp.html', context={
        "error": error,
        "isGuide": isGuide
    })


def signUpProcess(request):
    email = request.POST.get("email")
    name = request.POST.get("username")
    password = request.POST.get("password")
    confirmPassword = request.POST.get("confirmPassword")
    isGuide = request.POST.get('isGuide')

    if 'profile' in request.FILES:
        profile = request.FILES['profile']
        fs = FileSystemStorage()
        profileImage = fs.save(profile.name, profile)
        uploaded_img_url = fs.url(profileImage)
    else:
        request.session['error'] = 'Please Provide Profile Picture'
        return redirect('/signup')
    
    if email == '' or password == '' or confirmPassword == '' or name =='':
        request.session['error']='Please fill all the fields'
    else:
        if password == confirmPassword:
            try:
                user = User.objects.get(email=email)
                request.session['error'] = 'User already exists'

            except User.DoesNotExist:
                newUser = User(email = email,password=password,name=name,profile=uploaded_img_url)  #blue wale fields models ki h
                newUser.save()
                if isGuide == 'True':
                    url = '/signup-guide?q='+str(newUser.id)
                    return redirect(url)
                else:
                    return redirect('/login')
        
        else:
            request.session['error'] = 'Password do not match'

    return redirect('/signup')

def signupGuidePage(request):
    error = None
    if 'error' in request.session:
        error = request.session['error']
        request.session['error'] = None
    
    return render(request,'auth/signup_guide.html', context={
        "error": error
    })

def signupGuideProcess(request):

    return redirect('/')


## ---------------------------------
##   Home Page
## --------------------------------- 

def homePage(request):
    # guides = { "guides" : [
    #     {"name":"sourabh","rate":800},
    #     {"name": "sachin", "rate": 700},
    #     {"name": "rishabh", "rate": 600},
    # ]}
    # reviews = { "reviews": [
    #     {"name": "sourabh", "message": "hello"},
    #     {"name": "sachin", "message": "world"},
    #     {"name": "rishabh", "message": "!"},
    # ]}
    # isLoggedIn = False
    # username = request.session['username']
    # # request.session['image'] = ''
    # if username != '':
    #     isLoggedIn = True

    # return render(request,'homepage/homepage.html',context={
    #     "guides": guides,
    #     "reviews": reviews,
    #     "isLoggedIn": isLoggedIn,
    #     "details": {
    #         "username": username,
    #         "profile": request.session['image']
    #     }
    # })
    userid = ''
    if 'userid' in request.session:
        userid = request.session['userid']

    return render(request, 'homepage/homepage.html', context={
        "user": {
            "name": userid
        },
        "guides": [],
        "reviews": []
    })