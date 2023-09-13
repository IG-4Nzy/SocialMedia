from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import socialmedia
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import UpdateUserForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from .forms import ChatForm
from .models import Chat




def base(request):
    return render(request,'base.html')

@login_required
def home(request):
    current_user = request.user
    e = socialmedia.objects.filter(user=current_user).exclude(post__exact='')
    profile = socialmedia.objects.filter(user=current_user).first()  # Get the profile picture data
    context = {
        'c': e,
        'pic': profile  # Pass the profile picture data to the template context
    }
    return render(request, 'home2.html', context)
def changepass(request):
    return render(request,'changepassword.html')
def chat(request):
    return render(request,'chat.html')

@login_required
def post(request):
    if request.method == "POST":
        post = request.FILES.get('post')
        title = request.POST.get('title')
        content = request.POST.get('content')

        social_media = socialmedia(title=title, content=content, post=post, user=request.user)
        social_media.save()

        return redirect('home')

    posts = socialmedia.objects.filter(user=request.user).first()
    context = {
                'c': posts
            }
    return render(request, 'post.html',context)

@login_required
def profile(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        bio = request.POST.get('bio')

        social_media_objects = socialmedia.objects.filter(user=request.user)
        if social_media_objects.exists():
            social_media = social_media_objects.first()
        else:
            social_media = socialmedia(user=request.user)

        if pic:
            social_media.profilepicture = pic
        social_media.bio = bio
        social_media.save()

        return redirect('profile')

    profiles = socialmedia.objects.filter(user=request.user).first()
    context = {
        'pic': profiles
    }
    return render(request, 'profile.html', context)


@login_required
def settings(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user, request=request)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Replace 'settings' with the URL name of the settings page
    else:
        form = UpdateUserForm(instance=request.user, request=request)
    return render(request, 'settings.html', {'form': form})

def sign(request):
    return render(request,'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signin.html', {'key': "account credentials not match"})
    return render(request, 'signin.html')

def signup(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        p1 = request.POST.get('pass1')
        p2 = request.POST.get('pass2')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')

        if p1 == p2:
            if User.objects.filter(username=uname).exists():
                return render(request, 'signup.html', {'key': "User already exists"})
            else:
                user = User.objects.create_user(username=uname, password=p1, email=email)
                pic = request.FILES.get('pic')
                bio=request.POST.get('bio')
                social_media = socialmedia.objects.create(
                    user=user,
                    uname=uname,
                    pass1=p1,
                    fname=fname,
                    lname=lname,
                    email=email,
                )
                subject = 'Registration Confirmation'
                message = 'Thank you for using our social media application.'
                from_email = 'athulas733@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                login(request, user)




                return render(request, 'home2.html', {'user': user})
        else:
            return render(request, "signup.html", {'key': 'Passwords do not match'})

    return render(request, 'signup.html')

def userlist(request):
    users = User.objects.all()
    profiles = socialmedia.objects.filter(user__in=users)
    context = {
        'profiles': profiles,
        'users': users
    }
    return render(request, 'userlist.html', context)


def log(request):
    logout(request)
    return redirect('signin')

def send_message(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender = request.user
            chat = Chat(sender=sender, receiver=receiver, message=message)
            chat.save()
            return redirect('chat')
    else:
        form = ChatForm()
    
    return render(request, 'chat.html', {'form': form, 'receiver': receiver})

