from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from login import settings
from django.core.mail import send_mail
# Create your views here.

def home(request):
    return render(request,"login_page/index.html")


def signup(request): 
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password = request.POST['cpassword']
        
        if User.objects.filter(username=username):
            messages.error(request,"username already exist! Please try some other username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,"email is already exist")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request,"You username can't be that long")
            
        if password != password:
            messages.error(request,"password didn't match")

        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname 
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, "You Account has been succesfully created.")
        
        
        # subject = "Welcome to login_page"
        # messages = "hello" + myuser.first_name + "!! \n" + "Welcome to Login_Page. Check your email and spanna"
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject,messages, from_email, to_list, fail_silently =True)
        
        
        return redirect('signin')
        
    return render(request,"login_page/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username , password = password)
        
        if user is not None:
            login(request , user)
            fname = user.first_name 
            return render(request,"login_page/index.html", {'fname':fname})
            
        else:
            messages.error(request, "bad credentials!")
            return redirect('home')
        
    return render(request,"login_page/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')