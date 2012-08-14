from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from countries.models import *
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    birth_date   = models.DateField(_('Birthday'), null=True, blank=True)
    countries    = models.ForeignKey(Country, null=True, blank=True)
    user         = models.OneToOneField(User)
    profile_pic  = models.ImageField(upload_to='tmp/', null=True, blank=True)

    def __unicode__(self):
        return self.user.get_full_name()

admin.site.register(Profile)