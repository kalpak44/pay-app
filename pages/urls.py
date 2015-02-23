from django.conf.urls import patterns, include, url
from pages import views


urlpatterns = patterns('',
    # ex: page/
    url(r'^$', views.index, name='index'),
    # ex: page/5/
    url(r'^(?P<page_id>\d+)$', views.getPage, name='getPage'),
    # ex: page/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: page/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)