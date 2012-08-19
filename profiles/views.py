from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from profiles.forms import *
from profiles.models import Profile
from django.contrib.auth import logout
from datetime import date
from django.utils import simplejson
from fuzzywuzzy import fuzz

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
        form = RegistrationForm(initial={ 'username': 'Testing Stuff', 'password': '10','password1':'randomnumbers12345678910','email': 'okay@ble.com' })
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
    #check if it contains space if it does, then it must be a name
    #or partial name, else it can be a nickname too
    if (' ' in search_keyword) == True:
        search_keywords = search_keyword.split(' ')
        first  = ''.join(search_keywords[0])
        second = ''.join(search_keywords[1])
        users = User.objects.filter(( Q(first_name__icontains=first) & Q(last_name__icontains=second) )
                                  | (Q(first_name__icontains=second) & Q(last_name__icontains=first)))
    else:
        users = User.objects.filter(Q(username__icontains=search_keyword)
                                  | Q(first_name__icontains=search_keyword)
                                  | Q(last_name__icontains=search_keyword))
    response_data=[]
    for user in users:
        #check query similarities
        if fuzz.token_sort_ratio(user.get_full_name(), search_keyword) > fuzz.ratio(user.username, search_keyword):
            similarity=fuzz.token_sort_ratio(user.get_full_name(), search_keyword)
        else:
            similarity=fuzz.ratio(user.username, search_keyword)

        #bonus for living in the same area (country)
        if request.user.get_profile().countries == user.get_profile().countries:
            similarity += 10
        #remove 50 points for being yourself and if match is only partial found.
        if request.user == user and not ( user.get_full_name().lower() ==  search_keyword.lower()
                                       or user.username.lower() == search_keyword.lower()
                                       or user.last_name.lower()+' '+user.first_name.lower() == search_keyword.lower() ):
            similarity -= 50

        response_data +=[
             (user.username,
             user.get_full_name(),
             user.get_profile().profile_pic.url,
             similarity)
        ]
    #sort by similarity
    sorted_data=sorted(response_data, key=lambda a:a[3], reverse=True)
    return HttpResponse(simplejson.dumps(sorted_data[:10]), mimetype="application/json")

@login_required
def User_Profile_Edit(request):
    #TODO: ability to edit your profile.
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['profile_pic'])
            member = request.user.profile
            member.birth_date   = form.cleaned_data['birth_date']
            member.countries    = form.cleaned_data['countries']
            member.about_me     = form.cleaned_data['about_me']
            member.profile_pic  = form.cleaned_data['profile_pic']
            member.save();
        return render_to_response('edit.html', {}, context_instance=RequestContext(request))
    else:
        member = request.user.get_profile()
        data = {
            'birth_date': member.birth_date,
            'profile_pic': member.profile_pic,
            'countries': member.countries,
            'about_me': member.about_me
        }
        form = EditForm(initial=data)
        context= {
            'form': form
        }
        return render_to_response('edit.html', context, context_instance=RequestContext(request))

@login_required
def User_Profile_Friends(request, username=""):
    member = User.objects.get(username = username)
    friends = member.get_profile().friends

    context= {
        'friends': friends,
        'member': member,
    }
    return render_to_response('friends.html', context, context_instance=RequestContext(request))

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

def handle_uploaded_file(f):
    with open('media/tmp/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)