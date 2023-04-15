from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from . models import Profile,Post,Like ,Follower
from itertools import chain
import random

@login_required(login_url='signin')  #for security
def index(request):
    user_obj = User.objects.get(username=request.user.username)
    profile_user=Profile.objects.get(user=request.user)
    current=Post.objects.filter(user=request.user)

    following_list=[]
    feed=[]

    following_list_user=Follower.objects.filter(follower=request.user.username)
    for users in following_list_user:
        following_list.append(users.user)

    for username in following_list :
        feed_list=Post.objects.filter(user=username)
        feed.append(feed_list)
    feed.append(current)
    feed_lists=list(chain(*feed))


    #suggestions list
    all_user=User.objects.all()
    user_following_all=[]

    for users in following_list_user:
        user_list=User.objects.filter(username=users.user)
        user_following_all.append(user_list)

    new_sugg_list=[x for x in list(all_user)if(x not in list(user_following_all))]
    current_user=User.objects.filter(username=request.user.username)
    final_suggest_list=[x for x in list(new_sugg_list) if (x not in list(current_user))]
    random.shuffle(final_suggest_list)

    username_profile=[]
    username_profile_list=[]

    for users in final_suggest_list:
        username_profile.append(users.id)


    for ids in username_profile:
        user_prof=Profile.objects.filter(user__id=ids)
        username_profile_list.append(user_prof)

    user_prof_final_suggest=list(chain(*username_profile_list))

    context={'profile_user':profile_user ,
             'posts':feed_lists ,
             'user_prof_final_suggest':user_prof_final_suggest ,
             "user_obj":user_obj,
             }
    return render(request,'index.html',context)

@login_required(login_url='signin')  #for security
def setting(request):
    profile_user=Profile.objects.get(user=request.user)
    if request.method=="POST":
        if request.FILES.get("profile_pic") == None:
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            profile_pic=profile_user.profile_pic
            bio=request.POST['bio']
            location=request.POST['location']

            profile_user.first_name=first_name
            profile_user.last_name = last_name
            profile_user.profile_pic=profile_pic
            profile_user.bio=bio
            profile_user.location=location
            profile_user.save()

        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            profile_pic=request.FILES.get('profile_pic')
            bio = request.POST['bio']
            location = request.POST['location']

            profile_user.first_name = first_name
            profile_user.last_name = last_name
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


@login_required(login_url='signin')  #for security
def profile(request,pk):
    user_obj=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_obj)
    user_post=Post.objects.filter(user=pk)
    user_post_len=len(user_post)

    follower=request.user.username
    user=pk

    if Follower.objects.filter(follower=follower,user=user).first(): #first return the value of the queryset
        button = 'UnFollow'
    else:
        button = 'Follow'

    follower_user=len(Follower.objects.filter(user=pk))
    following_user=len(Follower.objects.filter(follower=pk))

    context={
        'user_obj':user_obj,
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_len':user_post_len,
        'button':button,
        'following_user':following_user,
        'follower_user': follower_user,
    }
    return render(request,'profile.html',context)


@login_required(login_url='signin')  #for security
def followercount(request):
    if request.method=="POST":
        user=request.POST['user']
        follower=request.POST['follower']

        follow= Follower.objects.filter(user=user , follower=follower).first()

        if follow == None:
            follower = Follower.objects.create(user=user, follower=follower)
            follower.save()
            return redirect(f"/profile/{user}/")
        else:
            follow.delete()
            return redirect(f"/profile/{user}/")
    else:
        return redirect("/")


@login_required(login_url='signin')  #for security
def search(request):
    user_obj=User.objects.get(username=request.user.username)
    profile_user=Profile.objects.get(user=user_obj)

    if request.method=="POST":
        username=request.POST['username']
        username_obj=User.objects.filter(username__contains=username)

        username_profile_list = []
        username_profile = []


        for users in username_obj:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_list = Profile.objects.filter(user__id=ids) #in profile model, user field(that have ForeignKey),bring id
            username_profile_list.append(profile_list)

        username_profile_list = list(chain(*username_profile_list))

        context={
            "profile_user":profile_user,
            'user_obj':user_obj,
            'username_profile_list':username_profile_list,
        }
    return render(request,'search.html', context)


def edit_post(request):
    pass

def delete(request):
    user = str(request.user)
    post_id = request.GET.get('post_id')
    posts_user = Post.objects.filter(id=post_id).first()
    user_post = posts_user.user
    if user_post == user:
        posts_user.delete()
        return redirect("/")
    else:

        return redirect("/")
