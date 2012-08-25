from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class WallPost(models.Model):
    poster      = models.ForeignKey(User, related_name="poster")
    post        = models.TextField(_("Post Contents"))
    posted_on   = models.DateTimeField(_('Posted On'), auto_now_add=True)
    liked_by    = models.ManyToManyField(User, related_name="liked by")
    hated_by    = models.ManyToManyField(User, related_name="hated by")

    def __unicode__(self):
        return self.poster.get_full_name() + ' on ' + datetime.strftime(self.posted_on, "%Y-%m-%d %H:%M:%S")

admin.site.register(WallPost)