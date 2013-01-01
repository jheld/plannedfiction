from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fictionProject.views.home', name='home'),
    # url(r'^fictionProject/', include('fictionProject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'accounts/',include('registration.backends.default.urls')),
            #           url(r'^/accounts/login/$',include('django.contrib.auth.views.login')),
)

from piece import views as pViews

urlpatterns += patterns('',
                        url(r'^$', pViews.index, name='index'),
                        url(r'^pieces/$', pViews.pieces, name='pieces'),
                        url(r'^pieces/(?P<pk>\d)/$',pViews.piece, name='piece'),
                        url(r'^pieces/(?P<p_pk>\d)/events/(?P<e_pk>\d)/$', pViews.event,name='event'),
                        url(r'^pieces/(?P<pk>\d)/eventTiming/$',pViews.eventTiming, name='eventTiming'),
                        url(r'^pieces/(?P<p_pk>\d)/characters/(?P<ch_pk>\d)/$', pViews.characters,name='character'),
                        url(r'^accounts/login/$',pViews.my_login,name='my_login'),
                        url(r'^logout/$',pViews.my_logout,name='my_logout'),

)
