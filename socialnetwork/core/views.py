from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from . models import Profile,Post,Like

@login_required(login_url='signin')  #for security
def index(request):
#    user_obj=User.objects.get(username=request.user.username)
    profile_user=Profile.objects.get(user=request.user)

    posts=Post.objects.all()
    return render(request,'index.html',{'profile_user':profile_user , 'posts':posts})

@login_required(login_url='signin')  #for security
def setting(request):
    profile_user=Profile.objects.get(user=request.user)
    if request.method=="POST":
        if request.FILES.get("profile_pic") == None:
            profile_pic=profile_user.profile_pic
            bio=request.POST['bio']
            location=request.POST['location']

            profile_user.profile_pic=profile_pic
            profile_user.bio=bio
            profile_user.location=location
            profile_user.save()

        else:
            profile_pic=request.FILES.get('profile_pic')
            bio = request.POST['bio']
            location = request.POST['location']

            profile_user.profile_pic = profile_pic
            profile_user.bio = bio
            profile_user.location = location
            profile_user.save()

            return redirect('setting')

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
                return redirect('setting')
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


@login_required(login_url='signin')  #for security
def upload(request):
    if request.method=="POST":
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']

        upload_post=Post.objects.create(user=user,postimg=image,caption=caption)
        upload_post.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')  #for security
def likepost(request):
    username=request.user.username
    post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)

    like_filter=Like.objects.filter(post_id=post_id,username=username).first()

    print(like_filter)
    if like_filter == None:
        new_like=Like.objects.create(post_id=post_id,username=username)
        new_like.save()

        post.likes =post.likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.likes = post.likes-1
        post.save()
        return redirect('/')


def profile(request,pk):
    user_obj=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_obj)
    user_post=Post.objects.filter(user=pk)
    user_post_len=len(user_post)

    context={
        'user_obj':user_obj,
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_len':user_post_len,
    }
    return render(request,'profile.html',context)

