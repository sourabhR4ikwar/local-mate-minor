from django.shortcuts import render, redirect, render_to_response, reverse
from .models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.dateparse import parse_date
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators import csrf



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

def logout(request):
    request.session['userid'] = ''
    request.session['username'] = ''
    return redirect('/')



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
                if isGuide == 'True':
                    newUser.isGuide = bool(isGuide)
                    newUser.save()
                    url = '/signup-guide?q='+str(newUser.id)
                    return redirect(url)
                else:
                    return redirect('/login')
        
        else:
            request.session['error'] = 'Password do not match'

    return redirect('/signup')

def signupGuidePage(request):
    userid = request.GET.get('q')
    error = None
    if 'error' in request.session:
        error = request.session['error']
        request.session['error'] = None
    
    return render(request,'auth/signup_guide.html', context={
        "error": error,
        "userid":userid
    })

def signupGuideProcess(request):
    userid = request.POST.get('userid')
    about_me = request.POST.get('about_me')
    i_will_show_you = request.POST.get('i_will_show_you')
    rate = request.POST.get('rate')
    location = request.POST.get('location')
    quote = request.POST.get('quote')
    languages = request.POST.get('languages')
    redirectUrl = '/signup-guide?q='+str(userid)

    if userid == '':
        request.session['error'] = 'Invalid User'
        return redirect(redirectUrl)
    
    if about_me == '' or rate == '' or location == '' or quote=='' or languages =='' or i_will_show_you == '':
        request.session['error'] = 'Please fill all the fields'
        return redirect(redirectUrl)

    if rate.isdigit() is False:
        request.session['error'] = 'Please enter valid rate'
        return redirect(redirectUrl)
    
    user = User.objects.get(id=userid)
    newGuide = Guide(userid=user,
                    location=location,
                    quote=quote,
                    rate=rate,
                    ratings=0,
                    i_will_show_you=i_will_show_you,
                    about_me=about_me,
                    languages=languages,
                    isAvailable=True)
    print(newGuide.__dict__)
    newGuide.save()
    return redirect('/login')


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
    guides = Guide.objects.all().order_by('-ratings')[:10]
    reviews = Reviews.objects.all().order_by('-rating')[:15]
    trips = Trips.objects.all().order_by('-reviews__rating')[:15]
    userid = ''
    if 'userid' in request.session:
        userid = request.session['userid']

    return render(request, 'homepage/homepage.html', context={
        "user": {
            "name": userid
        },
        "guides": guides,
        "trips": trips,
    })

## ---------------------------------
##   search
## --------------------------------- 

def search(request):
    query = request.GET.get('q',None)
    # guides = User.objects.all()
    guides = Guide.objects.filter(location__contains=query)
    return render(request, 'search/search.html', context={
        "guides": guides,
        "query": query
    })

    ## www.test.com/search?name=sourabh
    
## ---------------------------------
##   Profile Calls
## --------------------------------- 

def retrieveGuide(request, guideid):
    guide = Guide.objects.get(id=guideid)
    trips = Trips.objects.filter(guide=guide)
    return render(request, 'profile/guide.html', context={
        "guide": guide,
        "trips": trips
    })

def profile(request):
    userid = request.session['userid']
    user = User.objects.get(id=userid)
    trips = Trips.objects.filter(creator=user)
    currentTrip = Trips.objects.get(creator=user,isActive=True)
    return render(request, 'profile/user.html', context={
        "user": user,
        "trips": trips,
        "currentTrip": currentTrip
    })

    
## ---------------------------------
##   Create Trip Section
## --------------------------------- 
def createTrip(request, guideid):
    guide = Guide.objects.get(id=guideid)

    return render(request, 'createTrip/create-trip.html', context={
        "guide_id":guideid,
        "user_id": request.session['userid'],
        "location": guide.location
    })

def createTripHandler(request):
    guide_id = request.POST.get('guide_id')
    user_id = request.POST.get('user_id')
    location = request.POST.get('location')
    dateStart = parse_date(request.POST.get('dateStart'))
    dateEnd = parse_date(request.POST.get('dateEnd'))
    # dateStart = datetime.strptime(request.POST.get('dateStart'), "%Y-%m-%d").date()
    # dateEnd = datetime.strptime(request.POST.get('dateEnd'), "%Y-%m-%d").date()

    guide = Guide.objects.get(id=guide_id)
    user = User.objects.get(id=user_id)
    dateDiff = dateEnd - dateStart
    price= dateDiff.days * int(guide.rate)
    review = Reviews()
    review.save()
    trip = Trips(
        creator=user,
        guide=guide,
        location=location,
        dateStart=dateStart,
        dateEnd=dateEnd,
        price=price,
        reviews=review
    )
    trip.save()
    tripid = trip.id
    return redirect('/payment/'+str(tripid))


## ---------------------------------
##   Conversations
## --------------------------------- 

def conversations(request):
    tripId = request.GET.get('q')
    trip = Trips.objects.get(id=tripId)
    conversations = Conversations.objects.filter(trip=trip)
    user_id = request.session['userid']
    conversation_exists = False
    if conversations.count() != 0:
        conversation_exists = True

    if trip.creator.id == user_id:
        sender_id = user_id
        receiver_id = trip.guide.user.id
    else :
        sender_id = trip.guide.user.id
        receiver_id = user_id

    receiver = User.objects.get(id=receiver_id)

    return render(request, 'message/message.html', context={
        "conversations": conversations,
        "sender_id": sender_id,
        "trip_id": tripId,
        "receiver_id": receiver_id,
        "receiver": receiver,
        "conversations_exists": conversation_exists
    }) 

def send(request):
    trip_id = request.POST.get('trip_id')
    sender_id = request.POST.get('sender_id')
    receiver_id = request.POST.get('receiver_id')
    message = request.POST.get('message')
    trip = Trips.objects.get(id=trip_id)
    sender = User.objects.get(id=sender_id)
    receiver = User.objects.get(id=receiver_id)
    
    conversation = Conversations(
        trip=trip,
        sender=sender,
        receiver=receiver,
        message=message
    )

    conversation.save()

    return redirect('/conversations?q='+str(trip_id))

## ---------------------------------
##   Payment
## --------------------------------- 

def paymentL(request, tripId):
    return render(request, 'createTrip/payment.html', context={
        "trip_id": tripId
    })

def paymentHandler(request):
    tripId = request.POST.get('trip_id')
    trip = Trips.objects.get(id=tripId)
    trip.isActive = True
    trip.paymentVerified = True
    trip.save()
    return redirect('/profile')

def payment(request, tripId):
    trip = Trips.objects.get(id=tripId)
    MERCHANT_KEY = "rmcWXioP"
    key="rmcWXioP"
    SALT = "zhlJAgzh6u"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    action = ''
    posted={}
    # Merchant Key and Salt provided y the PayU.
    for i in request.POST:
        posted[i]=request.POST[i]
    hash_object = hashlib.sha256(bytes(tripId, 'utf-8'))
    txnid=hash_object.hexdigest()[0:20]
    hashh = ''
    posted['txnid']=txnid
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key']=key
    posted['amount'] = trip.price
    posted['firstname'] = trip.creator.name
    posted['email']= "sourabh.d.raikwar@gmail.com"
    posted['surl']= "http://127.0.0.1:8000/success"
    posted['furl'] = "http://127.0.0.1:8000/failure"
    posted['productinfo'] = trip.__dict__
    hash_string=''
    hashVarsSeq=hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string+=str(posted[i])
        except Exception:
            hash_string+=''
        hash_string+='|'
    hash_string+=SALT
    hashh=hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    action =PAYU_BASE_URL
    if(posted.get("key")!=None and posted.get("txnid")!=None and posted.get("productinfo")!=None and posted.get("firstname")!=None and posted.get("email")!=None):
        return render(request,'payment/current_datetime.html',context={"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"https://sandboxsecure.payu.in/_payment" })
    else:
        return render(request,'payment/current_datetime.html',context={"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"." })


@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount=request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    salt="GQs7yium"
    try:
        additionalCharges=request.POST["additionalCharges"]
        retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
    if(hashh !=posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ",txnid)
        print("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
    return render(request,'payment/sucess.html',context={"txnid":txnid,"status":status,"amount":amount})


@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    c.update(csrf(request))
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount=request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    salt=""
    try:
        additionalCharges=request.POST["additionalCharges"]
        retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
    if(hashh !=posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ",txnid)
        print("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
    return render(request,"payment/Failure.html",context=c)

