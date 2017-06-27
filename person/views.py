from django.shortcuts import render,redirect
from .models import User, Post
from django.http import HttpResponse, Http404
from pbkdf2 import crypt


def home(request):
    try:
        id=request.session['id']
        return redirect('/dashboard/')
    except KeyError:
        return render(request, 'person/home.html')

def login(request):
    return render(request, 'person/login.html')

def register(request):
    return render(request, 'person/register.html')


def log_auth(request):
    user=request.POST['username']
    pw=request.POST['password']

    try:
        db_user=User.objects.get(username=user)
        db_pw=db_user.password
        if db_pw==crypt(pw, db_pw):
            db_user.logged_in=True;
            request.session['username']=user
            request.session['password']=pw
            request.session['id']=db_user.id
            # return HttpResponse('Logged in!')
            return redirect('/dashboard/')
        else:
            return HttpResponse('Wrong username/password!')
    except User.DoesNotExist:
        return HttpResponse('Wrong username/password!')

def reg_check(request):
    name=request.POST['name']
    surname=request.POST['surname']
    email=request.POST['email']
    user=request.POST['username']
    pw=request.POST['password']

    enc_pw=crypt(pw, iterations=3600)

    try:
        User.objects.get(username=user)

        return  HttpResponse('Username already exists, please try again with different username.')

    except User.DoesNotExist:
        if name=='' or surname=='' or email=='' or user=='' or pw=='':
            return HttpResponse('Please fill in all the details.')
        else:
            new_user=User(name=name, surname=surname, email=email, username=user, password=enc_pw)
            new_user.save()
            return HttpResponse('User registered.')

def dashboard(request):
    try:
        user_id=request.session['id']
        posts=Post.objects.filter(author_id=user_id)
        return render(request, 'person/dashboard.html', {'posts': posts})
    except KeyError:
        return redirect('/')

def logout(request):
    del request.session['id']
    return redirect('/')

def like(request):
    post_id=request.POST['post_id']
    post=Post.objects.get(id=post_id)
    post.likes += 1
    post.save()
    return redirect(request.POST['referrer'])

def unlike(request):
    post_id = request.POST['post_id']
    post = Post.objects.get(id=post_id)
    if post.likes != 0:
        post.likes -= 1
        post.save()
        return redirect(request.POST['referrer'])
    else:
        return redirect(request.POST['referrer'])

def profile(request, username):
    try:
        user=User.objects.get(username=username)
        posts=Post.objects.filter(author_id=user.id)
        return render(request, 'person/profile.html', {'user_info': user, 'posts': posts})
    except User.DoesNotExist:
        raise Http404

def new_post(request):
    title=request.POST['title']
    content=request.POST['content']
    user=User.objects.get(id=request.session['id'])
    new_post=Post(author=user, title=title, content=content)
    new_post.save()
    return redirect('/dashboard/')

# TO DO:

# Post creating form - DONE
# Post like - DONE
# Post unlike - DONE
# FIX: Like/Dislike transition
# Encrypt Password
# User check with 3rd party module