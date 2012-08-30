from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'wall.views.Wall'),
    url(r'^logout', 'profiles.views.User_Profile_Logout'),
    url(r'^register$', 'profiles.views.User_Profile_Registration'),
    url(r'^registered$', 'profiles.views.User_Profile_Registration_Finished'),
    url(r'^login', 'profiles.views.User_Profile_Login'),
    url(r'^search/', 'profiles.views.User_Profile_Search'),
    url(r'^edit/$', 'profiles.views.User_Profile_Edit'),
    url(r'^friends/(?P<username>[\w]+)', 'profiles.views.User_Profile_Friends', name="friendlist"),
    url(r'^json/(?P<search_keyword>[\w ]+)', 'profiles.views.json_searching'),


    url(r'^profile/(?P<username>[\w]+)/add', 'profiles.views.Specific_User_Profile_Add', name="specific_add"),
    url(r'^profile/(?P<username>[\w]+)/remove', 'profiles.views.Specific_User_Profile_Remove', name="specific_remove"),
    url(r'^profile/(?P<username>[\w]+)', 'profiles.views.Specific_User_Profile_Show', name="specific_url"),
    url(r'^profile/$', 'profiles.views.User_Profile_Show'),


    url(r'^chat/(?P<username>[\w]+)/json/last/seen', 'messages.views.Chat_Last_Seen'),
    url(r'^chat/(?P<username>[\w]+)/json/last', 'messages.views.Chat_Last_Item_PK'),
    url(r'^chat/(?P<username>[\w]+)/json/seen', 'messages.views.Chat_Seen'),
    url(r'^chat/(?P<username>[\w]+)/json/(?P<message_id>[0-9]+)', 'messages.views.Chat_Specific_Message'),
    url(r'^chat/(?P<username>[\w]+)/json', 'messages.views.Chat_With_JSON'),
    url(r'^chat/(?P<username>[\w]+)', 'messages.views.Chat_With'),


    url(r'^wallpost/addPost$', 'wall.views.addWallPost', name="addWallPost"),
    url(r'^wallpost/addComment/(?P<PostID>[0-9]+)', 'wall.views.addWallComment', name="addWallComment"),
    url(r'^wallpost/deleteComment/(?P<PostID>[0-9]+)', 'wall.views.removeWallComment', name="deleteComment"),
    url(r'^wallpost/(?P<PostID>[0-9]+)/comments', 'wall.views.WallPostComments', name="ListComments"),
    url(r'^wallpost/(?P<pk>[0-9]+)/like$', 'wall.views.LikeWallPost', name="LikeWallPost"),
    url(r'^wallpost/(?P<pk>[0-9]+)/dislike$', 'wall.views.DislikeWallPost', name="DislikeWallPost"),
    url(r'^wallpost/(?P<pk>[0-9]+)$', 'wall.views.WallPost', name="specific_post"),


    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
urlpatterns += staticfiles_urlpatterns()