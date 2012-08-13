from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from profiles.forms import RegistrationForm, LoginForm
from profiles.models import Profile

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
    context = {
                'profiles' : user,
                'username' : username,
              }
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

def Specific_User_Profile_Show(request,username):
    user = User.objects.get(username=username)
    context = {
                'profiles' : user
              }
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

