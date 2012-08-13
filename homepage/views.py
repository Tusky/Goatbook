from django.shortcuts import render_to_response
from django.template import RequestContext

def HomePage(request):
    if request.user.is_authenticated():
        User = request.user
        context = { 'profiles' : User }
        return render_to_response('home.html', context, context_instance=RequestContext(request))
    return render_to_response('home.html')