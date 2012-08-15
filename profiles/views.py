from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from profiles.forms import RegistrationForm, LoginForm
from profiles.models import Profile
from django.contrib.auth import logout
from datetime import date
from django.utils import simplejson

def User_Profile_Registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
            user.save()
            profile = Profile(user = user, first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'], birth_date = form.cleaned_data['birth_date'])
            profile.save()
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
        context = { 'form' : form }
        return render_to_response('register.html', context, context_instance=RequestContext(request))

def User_Profile_Login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            profile = authenticate(username=username, password=password)
            if profile is not None:
                login(request, profile)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('login.html', { 'form': form }, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', { 'form': form }, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = { 'form' : form }
        return render_to_response('login.html', context, context_instance=RequestContext(request))

@login_required
def User_Profile_Show(request):
    user = request.user
    age = calculate_age(user.get_profile().birth_date)
    context = {
                'profiles' : user,
                'age':age,
                'friendable': "none",
              }
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

def Specific_User_Profile_Show(request,username):
    user = User.objects.get(username=username)
    age = calculate_age(user.get_profile().birth_date)
    context = {
                'profiles' : user,
                'age':age,
                'friendable': "none",
    }
    if not username == request.user.username:
        context['friendable']=Profile.objects.filter(user=request.user,friends=user).count

    return render_to_response('profile.html', context, context_instance=RequestContext(request))

@login_required
def User_Profile_Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def User_Profile_Search(request):
    if request.method == 'POST':
        search_keyword = request.POST['search_keyword']
        users = User.objects.filter(Q(username__icontains=search_keyword) | Q(first_name__icontains=search_keyword) | Q(last_name__icontains=search_keyword))
        context = {
            'search_results' : users
        }
        return render_to_response('search.html', context, context_instance=RequestContext(request))

@login_required
def Specific_User_Profile_Add(request,username):
    user  = User.objects.get(username=username)
    request.user.get_profile().friends.add(user)
    return HttpResponseRedirect('/profile/'+username)

@login_required
def Specific_User_Profile_Remove(request,username):
    user  = User.objects.get(username=username)
    request.user.get_profile().friends.remove(user)
    return HttpResponseRedirect('/profile/'+username)

def json_searching(request,search_keyword):
    users = User.objects.filter(Q(username__icontains=search_keyword) | Q(first_name__icontains=search_keyword) | Q(last_name__icontains=search_keyword))
    id = 0
    response_data={}
    for user in users:
        response_data[id] ={
            'username': user.username,
            'fullname': user.get_full_name(),
            'imageurl': user.get_profile().profile_pic.url,
        }
        id += 1
    #TODO: better results, rated results by similarity/closeness(same country)
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year