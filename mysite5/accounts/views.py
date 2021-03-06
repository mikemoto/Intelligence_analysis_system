#coding=utf-8
from django.shortcuts import render

from django.shortcuts import render_to_response,render,get_object_or_404    
from django.http import HttpResponse, HttpResponseRedirect    
from django.contrib.auth.models import User    
from django.contrib import auth  
from django.contrib import messages  
from django.template.context import RequestContext  
      
from django.forms.formsets import formset_factory  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  
      
from bootstrap_toolkit.widgets import BootstrapUneditableInput  
from django.contrib.auth.decorators import login_required 

#from accounts.models import UserProfile, create_user_profile
from WebPage.models import webpage
from accounts.forms import LoginForm, UserCreationForm, ProfileForm
from django.views.decorators.csrf import csrf_exempt
from WebPage.models import Favour

import random  

#def index(request):
#    mypages = webpage.objects.all()
#    return render_to_response('index.html', RequestContext(request, {'mypages': mypages}))

@csrf_exempt
def register(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render_to_response("register.html", {
            'form': form,
        })
    else:         
        form = UserCreationForm(request.POST)
        register_flag = True
        error_messages = []
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            password_again = request.POST.get('password_again', '')
            favour = request.POST.get('favour', '')
            email = request.POST.get('email', '')
 
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                error_messages.append(u'用户名已存在')
                register_flag = False

            if password != password_again:
                error_messages.append(u'两次密码不一致')
                register_flag = False

            if not register_flag:
                return HttpResponse(u'注册失败!') 
                #return render_to_response('register.html', 
                #    RequestContext(request, {'error_messages': error_messages,}))
            else:
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email)   
                user.save()
                #p = user.profile
                #p.cate = favour
                #p.save()
                return HttpResponse(u'注册成功')
                #return HttpResponseRedirect('next/') 
        else:  
            return render_to_response('register.html', RequestContext(request, {'form': form,}))   

@csrf_exempt
def register_next(request):    
    if request.method == 'GET':
        form = ProfileForm()
        return render_to_response("register_next.html", {
            'form': form,
        })
    else:
        form = ProfileForm(request.POST)
        if form.is_valid():
            UserProfile
            cate = request.POST.get('favour', '')          
            #user = user.profile.cate = cate   
            #user.save()
            return HttpResponseRedirect('/') 
        else:  
            return render_to_response('register_next.html', RequestContext(request, {'form': form,})) 
@csrf_exempt
def login(request):  
    if request.method == 'GET':  
        form = LoginForm()  
        return render_to_response('login.html', RequestContext(request, {'form': form,}))  
    else:  
        form = LoginForm(request.POST)  
        if form.is_valid():  
            username = request.POST.get('username', '')  
            password = request.POST.get('password', '')  
            user = auth.authenticate(username=username, password=password)  
            if user is not None and user.is_active:  
                auth.login(request, user)
                return HttpResponseRedirect('/accounts/index/')  
            else:  
                return render_to_response('login.html', RequestContext(request, {'form':form,'password_is_wrong':True}))  
        else:  
            return render_to_response('login.html', RequestContext(request, {'form': form,}))

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login/')
    else:
        if Favour.objects.filter(user=request.user):
            username = request.user.username

            mypages = webpage.objects.all().order_by('?')[0:10]
            favours = Favour.objects.filter(user=request.user)
            return render_to_response('index.html', 
                RequestContext(request, {'mypages': mypages, 'username': username, 'favours':favours}))
        else:
            return render_to_response('index.html', 
                RequestContext(request))

def favour(request, favour):
    favour_mypages = webpage.objects.filter(cate=favour).order_by('pub_time')
    favours = Favour.objects.filter(user=request.user)
    username = request.user.username
    return render_to_response('index.html', 
           RequestContext(request, {'mypages': favour_mypages, 'username': username, 'favours':favours}))
