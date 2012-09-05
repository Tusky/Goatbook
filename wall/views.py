from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.utils import simplejson
from wall.forms import WallPostForm, WallCommentForm
from wall.models import WallPost, WallComment
from profiles.models import Profile
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import date

@login_required
def Wall(request):
    limit = 3
    posts = WallPost.objects.filter(poster=request.user)
    friendList = Profile.objects.filter(user=request.user)
    for friends in friendList:
        for friend in friends.friends.all():
            #Join yours and each of your friends querysets into one.
            posts = posts | WallPost.objects.filter(poster=friend)

    posts = posts.order_by('posted_on').reverse()[:50]
    for post in posts:
       post.comments = WallComment.objects.filter(wallpost=post)

    context={
        'posts': posts,
        'wallpost': WallPostForm(),
        'wallcomment': WallCommentForm(),
        'sliceUp': ":%s" % limit,
        'sliceDown': "%s:" % limit
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

@login_required
def addWallPost(request):
    if request.method == "POST":
        form = WallPostForm(request.POST)
        if form.is_valid():
            newPost = WallPost.objects.create(poster=request.user, post = form.cleaned_data['wallpost'])
            newPost.save()
            return HttpResponse(simplejson.dumps({"response": "Ok"}), mimetype="application/json")

@login_required
def addWallComment(request, PostID):
    #commenter, comment, wallpost
    if request.method == "POST":
        form = WallCommentForm(request.POST)
        if form.is_valid():
            Post = WallPost.objects.get(pk = PostID)
            newComment = WallComment.objects.create(commenter = request.user, comment = form.cleaned_data['wallcomment'], wallpost=Post)
            newComment.save()
            return HttpResponseRedirect('/')
            return HttpResponse(simplejson.dumps({"response": PostID }), mimetype="application/json")
    else:
        return HttpResponse(simplejson.dumps({"response": "No, just no"}), mimetype="application/json")

def removeWallComment(request, PostID):
    try:
        comment = WallComment.objects.get(pk = PostID)
        comment.delete()
        return HttpResponse(simplejson.dumps({"response": "True" }), mimetype="application/json")
    except ObjectDoesNotExist:
        return HttpResponse(simplejson.dumps({"response": "False" }), mimetype="application/json")

def WallPostComments(request, PostID):
    response = []
    wallpost = WallPost.objects.get(pk = PostID)
    comments = WallComment.objects.filter(wallpost = wallpost)
    for comment in comments:
        if comment.commenter == request.user:
            ownComment = "True"
        else:
            ownComment = "False"
        response +=[
            (comment.pk, ownComment, comment.commenter.get_full_name(), reverse('specific_url', args=[comment.commenter.username]), comment.comment, date.strftime(comment.commented_on, "%Y-%m-%d %H:%M:%S")),
        ]
    return HttpResponse(simplejson.dumps({"response": "ok", "comments": response }), mimetype="application/json")

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

def singlePost(request, pk):
    wallpost = WallPost.objects.get(pk=pk)
    wallpost.comments = WallComment.objects.filter(wallpost=pk)

    limit = 2
    context = {
        'post': wallpost,
        'wallcomment': WallCommentForm(),
        'sliceUp': ":%s" % limit,
        'sliceDown': "%s:" % limit
    }
    return render_to_response("wallpost.html", context, context_instance=RequestContext(request))