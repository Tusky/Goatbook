from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from messages.models import Message
from messages.forms import Chat
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.core.urlresolvers import reverse

@login_required
def Chat_With(request, username):
    try:
        partner = User.objects.get(username=username)
        if request.method == 'POST':
            form = Chat(request.POST)
            if form.is_valid():
                message = Message.objects.create(sender=request.user,receipt=partner,message=form.cleaned_data['message'])
                message.save()
            return HttpResponse(simplejson.dumps({'response' : "ok"}), mimetype="application/json")
    except ObjectDoesNotExist:
        raise Http404

    form = Chat()
    context= {
        'form': form,
        'partner': partner,
        }
    return render_to_response('chat_with.html', context, context_instance=RequestContext(request))

@login_required
def Chat_With_JSON(request, username):
    messageList = []
    try:
        partner = User.objects.get(username=username)
        messages = Message.objects.filter( ( Q(sender=request.user) & Q(receipt=partner) ) | ( Q(sender=partner) & Q(receipt=request.user) ) ).order_by("sent").reverse()[:10]

        for message in messages:
            if type(message.seen).__name__ == 'datetime':
                seen = datetime.strftime(message.seen, "%Y-%m-%d %H:%M:%S")
            else:
                seen = "not"
            messageList += [
                (message.pk, message.sender.get_full_name(),message.sender.get_profile().profile_pic.url, reverse("specific_url", args={message.receipt.username}), message.message, datetime.strftime(message.sent, "%Y-%m-%d %H:%M:%S"), seen ),
            ]
        return HttpResponse(simplejson.dumps(messageList), mimetype="application/json")
    except ObjectDoesNotExist:
        raise Http404

@login_required
def Chat_Last_Item_PK(request, username):
    try:
        partner = User.objects.get(username=username)
        messages = Message.objects.filter( ( Q(sender=request.user) & Q(receipt=partner) ) | ( Q(sender=partner) & Q(receipt=request.user) ) ).latest("pk")
        lastmessage = (messages.pk, datetime.strftime(messages.sent, "%Y-%m-%d %H:%M:%S"))
        return HttpResponse(simplejson.dumps(lastmessage), mimetype="application/json")
    except ObjectDoesNotExist:
        raise Http404

@login_required
def Chat_Specific_Message(request, username, message_id):
    try:
        partner = User.objects.get(username=username)
        message = Message.objects.get( Q(pk=message_id) & ((Q(sender=request.user)&Q(receipt=partner)) | (Q(sender=partner)&Q(receipt=request.user))) )
        if type(message.seen).__name__ == 'datetime':
            seen = datetime.strftime(message.seen, "%Y-%m-%d %H:%M:%S")
        else:
            seen = "not"
        the_message = (message.pk, message.sender.get_full_name(),message.sender.get_profile().profile_pic.url, reverse("specific_url", args={message.receipt.username}), message.message, datetime.strftime(message.sent, "%Y-%m-%d %H:%M:%S"), seen )
        return HttpResponse(simplejson.dumps(the_message), mimetype="application/json")
    except ObjectDoesNotExist:
        raise Http404

@login_required
def Chat_Seen(request, username):
    try:
        partner = User.objects.get(username=username)
        messages = Message.objects.filter( Q(seen=None) & (Q(sender=partner)&Q(receipt=request.user)) )
        for message in messages:
            message.seen=datetime.now()
            message.save()
        return HttpResponse(simplejson.dumps({"response": "ok"}), mimetype="application/json")
    except ObjectDoesNotExist:
        raise Http404

def Chat_Last_Seen(request, username):
    try:
        partner = User.objects.get(username=username)
        message = Message.objects.filter( Q(sender=request.user) & Q(receipt=partner) ).exclude(seen=None)
        return HttpResponse(simplejson.dumps({"date": datetime.strftime(message.latest('seen').seen, "%Y-%m-%d %H:%M:%S")}), mimetype="application/json")
    except ObjectDoesNotExist:
        raise Http404

