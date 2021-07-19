from django.db import models
from django.http.response import HttpResponse 
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import registraion,exam
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re 
import razorpay
#below adding for email sending
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

def base(request):
    return render(request,'base.html')

def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')

def test(request):
    datas = exam.objects.all()
    # user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(datas, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'test.html', { 'message': users })




def quiz(request):
    datas = exam.objects.all()
    # user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(datas, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'quiz.html', { 'message': users })


def question(request):
    datas = exam.objects.all()
    if request.method == 'POST':
        ques = request.POST['question']
        optn1 = request.POST['option1']
        optn2 = request.POST['option2']
        optn3 = request.POST['option3']
        optn4 = request.POST['option4']
        ans = request.POST['answer']
        riyazi = exam(question=ques,option1=optn1,option2=optn2,option3=optn3,option4=optn4,answer=ans)
        riyazi.save()
        print("Data is saved in db")
        return render(request,'quiz.html',{"message":datas})
    return render(request,'question.html')
    # return render(request,'quiz.html')


def payment(request):
    if request.method == 'POST':
        client = razorpay.Client(auth=("rzp_test_k4dKLS5hNZx8t0", "D28crmRPGKxDY4HiFRFlU3zI"))
        return render(request,'instruction.html')

        # data ={
        # "order_amount" : "10000",
        # "order_currency" : 'INR'
        # }
        # order= client.order.create(data=data)
        # print(order)
        
        # order_receipt = 'order_rcptid_11'
        # notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL
    return render(request,'payment.html')
def instruction(request):
    return render(request,'instruction.html') #k old code correc


def register(request):
    data = registraion.objects.all()
    if request.method == 'POST':
        numbr = request.POST['Mobile']
        match2 = re.fullmatch('[6-9]\d{9}',numbr)
        emlid = request.POST['Email']
        match3 = re.fullmatch('\w[a-zA-Z0-9_.]*@[a-zA-Z0-9]+[.][a-zA-Z]+',emlid)
        if match2!=None and match3!=None:
            fname = request.POST['First_name']
            lname = request.POST['Last_name']
            add1 = request.POST['Address1']
            add2 = request.POST['Address2']
            city = request.POST['City']
            state = request.POST['State']
            pin = request.POST['Pincode']
            image = request.FILES['picture']
            if image:
                print("Image Available")
            else:
                print("Not Available")
            regs = registraion(Email=emlid,Mobile=numbr,First_name=fname,Last_name=lname,Address1=add1,Address2=add2,City=city,State=state,Pincode=pin,picture=image)
            regs.save()
            # the below code for email sent
            # subject = 'Welcome to Riyazi-Quiz'
            # message = f'Hi {regs.First_name}, thank you for registering in Riyazi-Quiz.'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [regs.Email, ]
            # send_mail( subject, message, email_from, recipient_list)

            print("Your are Registered and Email Send")
            return render(request,'payment.html')
        else:
            messages.warning(request,'Invalid Email_Id & Mobile Number, Please enter correct input')
            return redirect('register')      
    return render(request,'register.html') 

def javascript(request):
    return render(request,'javascript.html')

def signup(request):
    if request.method == 'POST':        
        emid = request.POST['email']
        match = re.fullmatch('\w[a-zA-Z0-9_.]*@[a-zA-Z0-9]+[.][a-zA-Z]+',emid)
        if match!=None:
            usrr = request.POST['username']
            fname = request.POST['first_name']
            lname = request.POST['last_name']          
            pwd = request.POST['password']
            if User.objects.filter(username=usrr).exists():
                messages.error(request,'Username already exist..Please choose another!')
                return redirect('signup')
            elif User.objects.filter(email=emid).exists():
                messages.error(request,'EmailID already exist..Please choose another!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=usrr, first_name=fname, last_name=lname, email=emid, password=pwd) #to be continue..
                user.save(); 
                messages.success(request,'User Created, Please SignIn')
                return redirect('login')
        else:
            messages.warning(request,'Invalid Email_ID! Please Enter Correct & Valid Email_ID')
            return redirect('signup')          
    else:
        return render(request,'signup.html') 

def login(request):
    if request.method=='POST':
        user_name=request.POST['username']
        pass_word = request.POST['password']
        user=auth.authenticate(username=user_name, password=pass_word)
        if user is not None:
            auth.login(request,user)
            # messages.info(request,"Welcome to home page!!!")
            return redirect('about')
            # return redirect('home')
        else:
            messages.warning(request,"Invalid Username or password! Please try again.")
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    # messages.success(request,'Please LogIn Again!!!')
    return redirect('home')