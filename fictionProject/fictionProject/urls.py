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
)

from piece import views as pViews

urlpatterns += patterns('',
                        url(r'^$', pViews.index, name='index'),
                        url(r'^pieces/$', pViews.pieces, name='pieces'),
                        url(r'^pieces/(?P<pk>\d)/$',pViews.piece, name='piece'),
                        url(r'^pieces/(?P<p_pk>\d)/events/(?P<e_pk>\d)/$', pViews.event,name='event'),
                        url(r'pieces/(?P<pk>\d)/eventTiming/$',pViews.eventTiming, name='eventTiming'),
)