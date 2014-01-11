from operator import eq
import json
import random
import datetime
from collections import OrderedDict

from django import template
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.defaultfilters import slugify

from bakery.views import BuildableDetailView
from ratelimit.decorators import ratelimit

from checkup.models import Survey, Assignment, Question, Answer, Comment
from checkup.models import Choice, QuestionGroupOrder, Respondent, FormRequest
from checkup.models import QuestionGroup
from checkup.forms import SurveyForm

NO_RESPONSE = "No response"

#Limit requests to this view to 1,200 per hour from one IP address
#for both GET and POST. If ratelimited, throw a 403.
@ratelimit(rate='1200/h', method=None, block=True)
def surveyform(request, assignment_id):
    assignment = get_object_or_404(Assignment, form_slug=assignment_id)
    
    # This variable is no longer used. It was initially developed
    # as a reference to the FormRequest for a separate view that would
    # change the object's page_loaded boolean to true.
    request_key = str(assignment.id) + str(hex(random.randint(100000, 999999)))
    # When behind a proxy, the first one is the client IP, otherwise it is in REMOTE_ADDR
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')
    referer = request.META.get('HTTP_REFERER') or ''
    user_agent = request.META.get('HTTP_USER_AGENT') or ''
    try:
        form_request = FormRequest.objects.create(key=request_key, assignment=assignment,
                                                    ip_address=ip_address, referer=referer,
                                                    user_agent=user_agent)
    except:
        form_request = FormRequest.objects.create(key=request_key, assignment=assignment,
                                                    ip_address='0.0.0.0', referer='Unknown',
                                                    user_agent='Unknown')
    
    form_request.save()

    complete_check = (list(assignment.questions.questions.all().order_by('id').values_list('id', flat=True))
        == list(assignment.answers.all().order_by('question__question__id').values_list('question__question__id', flat=True))
        and Comment.objects.filter(assignment=assignment).exists())

    if complete_check:
        return HttpResponseRedirect('/checkup/thanks/' + assignment.form_slug + '/')
    else:
        Answer.objects.filter(assignment=assignment).delete()
        Comment.objects.filter(assignment=assignment).delete()
    
    if request.method == 'POST':
        form = SurveyForm(request.POST, assignment=assignment)
        
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if 'question' in key:
                    question = Question.objects.get(pk=int(key.split('-')[1]))
                    group = assignment.questions
                    # We store the QuestionGroupOrder with the answer
                    # so we have access to questions and answers
                    # IN ORDER from the assignment model later
                    group_order = QuestionGroupOrder.objects.get(
                        question=question, group=group)
                    answer = Answer.objects.get_or_create(assignment=assignment, 
                        question=group_order, 
                        answer=Choice.objects.get(pk=int(value)))
                elif 'comment' in key:
                    comment = Comment.objects.get_or_create(assignment=assignment,
                        comment=value)

            complete_check = (list(assignment.questions.questions.all().order_by('id').values_list('id', flat=True))
                == list(assignment.answers.all().order_by('question__question__id').values_list('question__question__id', flat=True))
                and Comment.objects.filter(assignment=assignment).exists())

            if complete_check:
                assignment.survey_complete = True
                assignment.save()

            email_message = assignment.respondent.first_name + ' ' + assignment.respondent.last_name
            email_message += ' responded to the survey: ' + assignment.survey.name + '\n\n'
            email_message += 'Here are the respondent\'s answer(s): \n'
            for answer in assignment.answers.all():
                email_message += answer.question.question.question + '\n'
                email_message += answer.answer.choice + '\n'
            email_message += '\n'
            email_message += 'Here is the respondent\'s comment (if any): \n'
            email_message += assignment.comment.comment + '\n'

            try:
                send_mail('CheckUp survey form submitted!', 
                            email_message, 
                            settings.DEFAULT_FROM_EMAIL,
                            [assignment.reporter.user.email], 
                            fail_silently=True)
            except AttributeError:
                #If they didn't set up their server.
                pass

            return HttpResponseRedirect('/checkup/thanks/' + assignment.form_slug + '/')
    else:
        form = SurveyForm(assignment=assignment)

    context = {
        'form' : form,
        'assignment' : assignment,
        }
    return render(request, 'checkup/surveyform.html', context)

def thanks(request, assignment_id):
    assignment = get_object_or_404(Assignment, form_slug=assignment_id)
    
    context = {
        'assignment' : assignment,
        }
    return render(request, 'checkup/thanks.html', context)

def survey_feed(request, slug):
    survey = get_object_or_404(Survey, home_slug=slug)
    survey_values = ['id','display_chatter','name']
    data = Survey.objects.filter(pk=survey.id).values(*survey_values)[0]
    
    # Get first assignment to appear after questions
    data['first_assignment'] = survey.first_assignment().get_absolute_url()

    assignments = OrderedDict()
    for assignment in survey.assignments.all():
        new_assign = {}

        new_assign_values = ['display_chatter', 'id', 'survey_complete', 
            'respondent_id', 'respondent__title__short', 'respondent__party',
            'respondent__headshot', 'respondent__last_name'];

        new_assign = Assignment.objects.filter(pk=assignment.id).values(*new_assign_values)[0]
        new_assign['url'] = assignment.get_absolute_url();
        new_assign['comment_left'] = True if (hasattr(assignment, 'comment') and assignment.comment.comment != '') else False
        
        qas = {}
        for q in assignment.questions.questions.all():
            if Answer.objects.filter(assignment=assignment, question__question=q).exists():
                a = Answer.objects.get(assignment=assignment, question__question=q)
                qas['%s' % q.question] = a.answer.choice
            else:
                qas['%s' % q.question] = NO_RESPONSE
        
        new_assign['qas'] = qas
    
        assignments['%s-%s' % (str(assignment.respondent.title.order).zfill(3), str(assignment.id).zfill(3))] = new_assign
    
    data['assignments'] = assignments
    data = json.dumps(data, sort_keys=False, indent=4)
    return HttpResponse(data, mimetype='application/json')
    
def overview_feed(request, slug):
    '''
    Overview feed contains:
    Survey info: id, display_chatter, name, feed_updated, number of respondents and number who completed
    Question info: id, question, number of respondents who chose each answer and who did not respond
        for each question.
    '''
    survey = get_object_or_404(Survey, home_slug=slug)
    survey_values = ['id','display_chatter','name']
    data = Survey.objects.filter(pk=survey.id).values(*survey_values)[0]
    data['survey_respondents'] = Assignment.objects.filter(survey=survey).count()
    data['surveys_complete'] = Assignment.objects.filter(survey=survey, survey_complete=True).count()
    
    questions = Question.objects.filter(questiongroup__in=QuestionGroup.objects.filter(assignment__survey=survey).distinct()).distinct()
    
    questions_dict = OrderedDict()
    
    data['bin_map'] = { NO_RESPONSE: 'no-response' }
    
    for q in questions:
        new_q_values = ['id', 'question', 'explanation', 'directed_to', 'visualize']
        new_q = Question.objects.filter(pk=q.id).values(*new_q_values)[0]
        
        new_q['asked'] = Assignment.objects.filter(survey=survey, questions__questiongrouporder__question=q).count()
        new_q['answered'] = Answer.objects.filter(assignment__survey=survey, question__question=q).count()
        new_q['no_answer'] = new_q['asked'] - new_q['answered']
        new_q['answers'] = {}
        new_q['bins'] = OrderedDict()
        
        for a in q.choices.all():
            new_q['answers']['%s' % a.choice] = Answer.objects.filter(assignment__survey=survey, question__question=q, answer=a).count()
            new_q['bins'][a.display.slug] = {'label': a.display.display}
            data['bin_map'][a.choice] = a.display.slug
        
        questions_dict['%s' % str(q.id)] = new_q
        
    data['questions'] = questions_dict
    
    data['feed_updated'] = str(datetime.datetime.now())
    
    data = json.dumps(data, sort_keys=False, indent=4)
    return HttpResponse(data, mimetype='application/json')

base_template = settings.TEMPLATE_BASE if hasattr(settings, 'TEMPLATE_BASE') else "checkup/base.html"

class BaseView(BuildableDetailView):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseView, self).get_context_data(*args, **kwargs)
        context['base_template'] = base_template
        return context

class SurveyDetail(BaseView):
    queryset = Survey.objects.all()
    slug_field = 'home_slug'
    context_object_name = 'survey'
    template_name = 'checkup/survey.html'

class AssignmentDetail(BaseView):
    queryset = Assignment.objects.all()
    slug_field = 'display_slug'
    context_object_name = 'assign'
    template_name = 'checkup/profile.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(AssignmentDetail, self).get_context_data(*args, **kwargs)
        try:
            job_desc = "checkup/job-descs/%s.html" % slugify(context['assign'].respondent.title.short)
            template.loader.get_template(job_desc)
        except template.TemplateDoesNotExist:
            job_desc = ""
        
        context['job_desc'] = job_desc
        return context
