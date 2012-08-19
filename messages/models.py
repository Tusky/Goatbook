from django.db import models
from django.contrib import admin
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Message(models.Model):
    sender      = models.ForeignKey(User, related_name="sender")
    receipt     = models.ForeignKey(User, related_name="receipt")
    message     = models.TextField(_('Message'))
    sent        = models.DateTimeField(auto_now_add=True)
    seen        = models.DateTimeField(_('Seen'), null=True, blank=True)

    def __unicode__(self):
        sent = datetime.strftime(self.sent, "%Y-%m-%d %H:%M:%S")
        return self.sender.first_name+' to '+self.receipt.first_name+' on '+sent

admin.site.register(Message)