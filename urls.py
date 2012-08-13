from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Goatbook.views.home', name='home'),
    # url(r'^Goatbook/', include('Goatbook.foo.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'homepage.views.HomePage'),
    url(r'^logout', 'profiles.views.User_Profile_Logout'),
    url(r'^register', 'profiles.views.User_Profile_Registration'),
    url(r'^login', 'profiles.views.User_Profile_Login'),
    url(r'^profile/(?P<username>\w{1,50})', 'profiles.views.Specific_User_Profile_Show'),
    url(r'^profile/$', 'profiles.views.User_Profile_Show'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()