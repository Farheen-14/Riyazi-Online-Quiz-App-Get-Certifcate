from django.db import models
from django.http import request
from django.http.response import HttpResponse 
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import contact_me, registraion,exam
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re 
import razorpay
#below adding for email sending
from django.conf import settings
from django.core.mail import send_mail
import pdfkit

# below for generating pdf 
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa




# Create your views here.
     
def home(request):
    return render(request,'home.html')

def base(request):
    return render(request,'base.html')

def about(request):
    return render(request,'about.html')


def certificate(request):
    template_path = 'certificate.html'
    details = registraion.objects.filter(user=request.user).last()
    context = {
        'data':details
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if download then below code use
    # response['Content-Disposition'] = 'attachment; filename="Riyazi-Quiz_Certificate.pdf"'
    # if display then  below code used
    response['Content-Disposition'] = 'filename="Riyazi-Quiz_Certificate.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # creating a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def footer1(request):
    enquiry_mail = contact_me.objects.all()
    if request.method == 'POST': 
        enqmail = request.POST['user_mail']
        enqname = request.POST['user_name']
        enqmsg = request.POST['user_message']
        enquiry = contact_me(user_mail=enqmail,user_message=enqmsg,user_name=enqname)
        enquiry.save()
        print("Your enquiry is submitted")
        # email sending
        subject = 'User Enquiry From Riyazi-Quiz'
        message = f'Hi, Riyazi-Quiz \n{enquiry.user_message}, \nThank & Regards \n{enquiry.user_name}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [enquiry.user_mail, ]
        send_mail( subject, message, email_from, recipient_list)
        print("Your are Registered and Email Send")
        # return render(request,'instruction.html')
    # return render(request,'footer1.html')
    return render(request,'about.html')



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
        return render(request,'register.html')
    return render(request,'payment.html')

def instruction(request):
    # obj = registraion.objects.get(user=request.user) only one data will receive
    obj = registraion.objects.filter(user=request.user).last() #last user login will shown
    # print(obj)
    # print(obj.First_name)
    return render(request,'instruction.html',{'data':obj}) 


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
            regs = registraion(user=request.user,Email=emlid,Mobile=numbr,First_name=fname,Last_name=lname,Address1=add1,Address2=add2,City=city,State=state,Pincode=pin,picture=image)
            regs.save()
            print("Your form is submitted")
             # the below code for email sending
            subject = 'Welcome to Riyazi-Quiz'
            message = f'Hi {regs.First_name}, \nThank you for registering in Riyazi-Quiz.\nNow, You are eligiable for online quiz.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [regs.Email, ]
            send_mail( subject, message, email_from, recipient_list)
            print("Your are Registered and Email Send")
            return render(request,'instruction.html')
        else:
            messages.warning(request,'Invalid Email_Id & Mobile Number, Please enter correct input')
            return redirect('register')      
    return render(request,'register.html') 

def congrats(request):
    return render(request,'congrats.html')

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
        else:
            messages.warning(request,"Invalid Username or password! Please try again.")
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request): 
    auth.logout(request)
    messages.success(request,'Successfully logout..you want login again?')
    return redirect('login')