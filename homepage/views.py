from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def HomePage(request):
    if request.user.is_authenticated():
        Users = request.user.get_profile()
        context = { 'profiles' : Users }
        return render_to_response('index.html', context, context_instance=RequestContext(request))
    context = {'profiles': "hey" }
    return render_to_response('index.html', context, context_instance=RequestContext(request))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')