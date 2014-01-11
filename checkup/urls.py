from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from checkup import views

urlpatterns = patterns('',
    # Survey-side
    url(r'^forms/(?P<assignment_id>\d+-\w+)/$', views.surveyform, name='surveyform'),
    url(r'^thanks/(?P<assignment_id>\d+-\w+)/$', views.thanks, name='thanks'),
    
    # Display-side
    url(r'^(?P<survey_slug>[\w-]+)/(?P<slug>[\d]+-[\w-]+)/$',
        login_required(views.AssignmentDetail.as_view()),
        name='assignment_detail'),
    url(r'^(?P<slug>[\w-]+)/$', 
        login_required(views.SurveyDetail.as_view()),
        name='survey_detail'),
    url(r'^(?P<slug>[\w-]+)/feed.json$', 
        views.survey_feed,
        name='survey_feed'),
    url(r'^(?P<slug>[\w-]+)/overview_feed.json$', 
        login_required(views.overview_feed),
        name='overview_feed'),
)