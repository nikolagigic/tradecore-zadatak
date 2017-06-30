from django.shortcuts import render,redirect, get_object_or_404
from .models import User, Post, Like, LookupUserInfo
from django.http import HttpResponse, Http404
from pyhunter import  PyHunter
import jwt
import clearbit


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
        enc_db_pw=db_user.password
        db_pw=jwt.decode(enc_db_pw, 'tradecore', algorithms=['HS256'])['password']
        if pw==db_pw:
            db_user.logged_in=True
            db_user.save()
            request.session['username']=user # Kreira se Cookie sa bitnim informacijama.
            request.session['password']=pw
            request.session['id']=db_user.id
            request.session[db_user.username]=db_user.username
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

    api=PyHunter("4f5c8bb9c0be022a99d1b860147701a642b03dbe")
    check=api.email_verifier(email)

    if not check['result']=='undeliverable':

        enc_pw=jwt.encode({'password': pw}, 'tradecore', algorithm='HS256') # 'tradecore' je kljuc po kom sifruje/desifruje pw,
                                                                                                                                                                 # moze se promeniti, ali je bitno da se isti kljuc
                                                                                                                                                                 # koristi tokom obe transakcije

        try:
            User.objects.get(username=user)

            return  HttpResponse('Username already exists, please try again with different username.')

        except User.DoesNotExist:
            if name=='' or surname=='' or email=='' or user=='' or pw=='':
                return HttpResponse('Please fill in all the details.')
            else:
                new_user=User(name=name, surname=surname, email=email, username=user, password=enc_pw)
                new_user.save()
                clearbit.key='sk_616a2b4b6e5b0999cd2e3ad727b701d1'
                find_info=clearbit.Person.find(email=email)
                if find_info: # U slucaju da ne pronalazi nista ili izbaci KeyError u vise navrata, promenite API Key, koristeci svoj, s obzirom da je moj dalog free i imam ogranicen broj provera.
                    lookup_info=LookupUserInfo( # KeyError izbacuje u slucaju da find_info vrati None type(odnosno da lookup nije ni odradjen), mada bi if statement trebao da zaobidje to, desava se u retkim slucajevima da vrati KeyError
                        user=User.objects.get(username=user), # Sto se tice informacija, izvlacio sam samo bitne vrednosti.
                        givenName=find_info['name']['givenName'],
                        familyName=find_info['name']['familyName'],
                        email=find_info['email'],
                        gender=find_info['gender'],
                        location=find_info['location'],
                        timeZone=find_info['timeZone'],
                        bio=find_info['bio'],
                        site=find_info['site'],
                    )
                    lookup_info.save()
                return HttpResponse('User registered.')

    else:
        return HttpResponse('E-mail is not valid. Please use the valid email.')

def dashboard(request):
    try:
        user_id=request.session['id']
        user_full_name = User.objects.get(id=user_id).name + ' ' + User.objects.get(id=user_id).surname
        posts=Post.objects.filter(author_id=user_id)
        return render(request, 'person/dashboard.html', {'posts': posts, 'full_name':user_full_name})
    except User.DoesNotExist:
        del request.session['id']
        return  redirect('/')
    except KeyError:
        return redirect('/')

def logout(request):
    try:
        logged_in=User.objects.get(id=request.session['id'])
        logged_in.logged_in=False
        logged_in.save()
        del request.session['id']
        return redirect('/')
    except User.DoesNotExist:
        del request.session['id']
        return redirect('/')
    except KeyError:
        return redirect('/')

def like(request):
    post_id=request.POST['post_id']
    post=Post.objects.get(id=post_id)
    new_like=Like.objects.get_or_create(user=User.objects.get(id=request.session['id']), post=post)

    if new_like[1]==False: # get_or_create(obj, Boolean) -> False u slucaju da obj vec postoji.
        if new_like[0].like==True:
            post.likes-=1
            new_like[0].like=False
            new_like[0].save()
            post.save()
        else:
            post.likes+=1
            new_like[0].like=True
            new_like[0].save()
            post.save()
    else:
        post.likes+=1
        new_like[0].like = True
        new_like[0].save()
        post.save()

    return  redirect(request.POST['referrer'])

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
# FIX: Like/Dislike transition - DONE
# Encrypt Password - DONE
# User check with 3rd party module - DONE