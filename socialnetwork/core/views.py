from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from . models import Profile

@login_required(login_url='signin')  #for security
def index(request):
    return render(request,'index.html')

@login_required(login_url='signin')  #for security
def setting(request):
    profile_user=Profile.objects.get(user=request.user)
    return render(request,'setting.html',{'profile_user':profile_user})


def signup(request):

    if request.method=="POST":
        username =request.POST['username']
        email =request.POST['email']
        password =request.POST['password']
        password2=request.POST['password2']
        print(password , password2)
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'message taken')
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request,"username taken")
                return redirect("signup")
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()

                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                user_model=User.objects.get(username=username)  #set username as defult in profile
                new_profile=Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request,'passwprd not match')
            return redirect('signup')
    else:
        return render(request,'signup.html')

"""        if request.method=="POST":
                form=SignupForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponse("sucess")
            else:
                return render(request, 'signup.html')"""

def signin(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Credentials Invalid")
            return redirect('signup')
    else:
        return render(request,'signin.html') #render need html

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect("signin")

