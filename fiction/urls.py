"""fiction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from piece import views as pViews
from event import views as eViews
from subject import views as sViews
from userAccount import views as uaViews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]


urlpatterns += [
    url(r'^$', pViews.index, name='index'),
    url(r'^pieces/$', pViews.PiecesListView.as_view(), name='pieces'),
    url(r'^pieces/(?P<pk>\d)/$', pViews.piece, name='piece'),
    # url(r'^pieces/(?P<p_pk>\d)/events/(?P<e_pk>\d)/$', eViews.event,name='event'),
    url(r'^pieces/(?P<p_pk>\d)/events/(?P<e_pk>\d)/$', eViews.EventDetailView.as_view(), name='event'),
    url(r'^pieces/(?P<pk>\d)/eventTiming/$', eViews.eventTiming, name='eventTiming'),
    # url(r'^pieces/(?P<p_pk>\d)/characters/(?P<ch_pk>\d)/$', sViews.characters,name='character'),
    url(r'^pieces/(?P<p_pk>\d)/characters/(?P<ch_pk>\d)/$', sViews.CharacterDetailView.as_view(), name='character'),
    url(r'^accounts/login/$', uaViews.my_login, name='my_login'),
    url(r'^logout/$', uaViews.my_logout, name='my_logout'),
]