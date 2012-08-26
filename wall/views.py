from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.utils import simplejson
from wall.forms import WallPostForm
from wall.models import WallPost
from profiles.models import Profile
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def Wall(request):
    limit = 3
    posts = WallPost.objects.filter(poster=request.user)
    friendList = Profile.objects.filter(user=request.user)
    for friends in friendList:
        for friend in friends.friends.all():
            #Join yours and each of your friends querysets into one.
            posts = posts | WallPost.objects.filter(poster=friend)
    context={
        'posts': posts.order_by('posted_on').reverse()[:50],
        'form': WallPostForm(),
        'sliceUp': ":%s" % limit,
        'sliceDown': "%s:" % limit,
    }
    return render_to_response("wall.html", context, context_instance=RequestContext(request))

@login_required
def LikeWallPost(request, pk):
    try:
        wallpost = WallPost.objects.get(Q(pk=pk) & Q(liked_by=request.user))
        wallpost.liked_by.remove(request.user)
        wallpost.save()
        liked, disliked=getPostLikesAndDislikes(pk)
        return HttpResponse(simplejson.dumps({"response": "removed", "liked_by": liked, "hated_by": disliked}), mimetype="application/json")
    except ObjectDoesNotExist:
        try:
            #todo: check for if you can even see the post/have permission to see it.
            wallpost = WallPost.objects.get(pk=pk)
            wallpost.liked_by.add(request.user)
            wallpost.hated_by.remove(request.user)
            wallpost.save()
            liked, disliked=getPostLikesAndDislikes(pk)
            return HttpResponse(simplejson.dumps({"response": "liked", "liked_by": liked, "hated_by": disliked}), mimetype="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(simplejson.dumps({"response": "false"}), mimetype="application/json")

@login_required
def DislikeWallPost(request, pk):
    try:
        wallpost = WallPost.objects.get(Q(pk=pk) & Q(hated_by=request.user))
        wallpost.hated_by.remove(request.user)
        wallpost.save()
        liked, disliked=getPostLikesAndDislikes(pk)
        return HttpResponse(simplejson.dumps({"response": "removed", "liked_by": liked, "hated_by": disliked}), mimetype="application/json")
    except ObjectDoesNotExist:
        try:
            #todo: check for if you can even see the post/have permission to see it.
            wallpost = WallPost.objects.get(pk=pk)
            wallpost.hated_by.add(request.user)
            wallpost.liked_by.remove(request.user)
            wallpost.save()
            liked, disliked=getPostLikesAndDislikes(pk)
            return HttpResponse(simplejson.dumps({"response": "disliked", "liked_by": liked, "hated_by": disliked}), mimetype="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(simplejson.dumps({"response": "false"}), mimetype="application/json")


def getPostLikesAndDislikes(pk):
    wallpost = WallPost.objects.get(pk=pk)
    liked_by = wallpost.liked_by.all()
    hated_by = wallpost.hated_by.all()
    liked, disliked="", ""
    i, j=1, 1
    for likes in liked_by:
        if i == liked_by.count():
            liked += likes.get_full_name()
        else:
            liked += likes.get_full_name()+","
        i+=1
    for dislikes in hated_by:
        if j == hated_by.count():
            disliked += dislikes.get_full_name()
        else:
            disliked += dislikes.get_full_name()+","
        j+=1
    return liked, disliked
