from wall.models import WallPost
from profiles.models import Profile
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

def Wall(request):
    posts = WallPost.objects.filter(poster=request.user)
    friendList = Profile.objects.filter(user=request.user)
    for friends in friendList:
        for friend in friends.friends.all():
            #Join yourself and each of your friends querysets into one.
            posts = posts | WallPost.objects.filter(poster=friend)
    context={
        'posts': posts.order_by('posted_on').reverse()[:50],
    }
    return render_to_response("wall.html", context, context_instance=RequestContext(request))


