import random
from operator import eq

from django.db import models
from localflavor.us.models import USStateField, USPostalCodeField, PhoneNumberField
from localflavor.us.us_states import USPS_CHOICES
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import slugify
from django.template.loader import select_template

from django.db.models.signals import post_delete
from django.dispatch import receiver


try:
	PARTIES = settings.POLITICAL_PARTIES
except NameError:
	PARTIES = (
		('REP', 'Republican'),
		('DEM', 'Democract'),
	)
	
class Reporter(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	title = models.ForeignKey('Title', help_text='Optional title to appear before reporter\'s name.',  blank=True)
	phone = PhoneNumberField(blank=True)
	
	def __unicode__(self):
		return self.user.username

class Survey(models.Model):
	name = models.CharField(max_length=150, unique=True)
	form_chatter = models.TextField(help_text='Optional, all respondents read this before filling out form (you can set chatter for specific respondents when creating an assignment).', blank=True)
	home_slug = models.SlugField(unique=True, default='')
	
	display_chatter = models.TextField(help_text='Optional, readers read this before reading survey responses.', blank=True)
	display_byline = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.name
	
	def first_assignment(self):
		return self.assignments.order_by(
			'-survey_complete', 'respondent__title__order', 'respondent__last_name', 'id')[0]
	
	@models.permalink
	def get_absolute_url(self, *args, **kwargs):
		return ('survey_detail', [self.home_slug], {},)
		
class Group(models.Model):
    name = models.CharField(max_length=75, unique=True)
    
    def __unicode__(self):
            return self.name

class Title(models.Model):
	short = models.CharField(max_length=75, help_text='Used for smaller spaces. U.S. Sen. or San Diego D.A.')
	long = models.CharField(max_length=75, help_text='Examples: United States Senator or San Diego District Attorney.')
	order = models.PositiveSmallIntegerField(default=0, help_text='Lower order is a higher rank. So, president is 0 and village clerk is 50')

	class Meta:
		unique_together = (('short', 'long'),)
		ordering = ['order',]

	def __unicode__(self):
		return self.long

class Respondent(models.Model):
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	group = models.ForeignKey('Group', help_text='A group of respondents that may be asked the same questions, i.e. Nassau County Legislator')
	title = models.ForeignKey('Title', help_text='Displayed next to a person\'s name')
	party = models.CharField(max_length=3, choices=PARTIES, 
		help_text='Optional, the party of the person. This is used in legislative suffixes (R-Hempstead) ONLY when a district is also specified below.', 
		blank=True)
	district = models.CharField(max_length=75, 
		help_text='Optional legislative district. If both party and district are specified, a suffix (R-Hempstead) may appear after the legislator\'s name',
		blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	first_name = models.CharField(max_length=75)
	last_name = models.CharField(max_length=75)
	website = models.URLField(max_length=254, blank=True)
	office_phone = PhoneNumberField(blank=True, help_text='The number the public calls to talk with this person.')
	email = models.EmailField(max_length=254, blank=True)
	twitter = models.CharField(max_length=75, blank=True)
	address = models.CharField(max_length=150, help_text='Public mailing address.', blank=True)
	address2 = models.CharField(max_length=150, blank=True)
	city = models.CharField(max_length=75, blank=True)
	state = USPostalCodeField(blank=True)
	zip = models.CharField(max_length=5, blank=True)
	headshot = models.URLField(max_length=255, blank=True, help_text='URL of head shot image')
	contact_name = models.CharField(max_length=150, 
		help_text='Name of their spokesperson or other assistant (or the respondent if you have non-public contact information).', 
		blank=True)
	contact_phone = PhoneNumberField(blank=True)
	contact_email = models.EmailField(max_length=254, blank=True)
	#Extra ID field for use in synchronizing respondents/assignments from a spreadsheet.
	sheet_id = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.title.short + ' ' + self.first_name + ' ' + self.last_name
	
	def full_name(self):
		return self.first_name + ' ' + self.last_name
	
	class Meta:
		ordering = ['title', 'last_name',]

class Question(models.Model):
	question = models.TextField()
	explanation = models.TextField(blank=True, help_text='Provide more information about this question.')
	directed_to = models.CharField(max_length=150, blank=True, default="", help_text='A short description of who this question is going to (e.g., "State Lawmakers")')
	choices = models.ManyToManyField('Choice')
	visualize = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.question


class ChoiceDisplay(models.Model):
	slug = models.SlugField()
	display = models.TextField(blank=True)
	no_answer = models.BooleanField(default=False, help_text="bucket represents the 'no answer' option.")
	order = models.PositiveSmallIntegerField(default=1)
	
	def __unicode__(self):
		return self.slug

class Choice(models.Model):
	display = models.ForeignKey(ChoiceDisplay)
	choice = models.CharField(max_length=75, unique=True)
	
	def __unicode__(self):
		return self.choice
	
	class Meta:
		ordering = ('-display__order',)
	

class QuestionGroup(models.Model):
	name = models.CharField(max_length=75, unique=True)
	questions = models.ManyToManyField('Question', through='QuestionGroupOrder')
	
	def __unicode__(self):
		return self.name

class QuestionGroupOrder(models.Model):
	group = models.ForeignKey('QuestionGroup')
	question = models.ForeignKey('Question')
	order = models.PositiveSmallIntegerField()
	
	class Meta:
		ordering = ['order']
	
	def __unicode__(self):
		return str(self.order) + ' - ' + self.question.question


class Assignment(models.Model):
	survey = models.ForeignKey('Survey', related_name='assignments')
	respondent = models.ForeignKey('Respondent', related_name='assignments')
	reporter = models.ForeignKey('Reporter', help_text='Reporter assigned to contact respondent for this survey.', blank=True)
	questions = models.ForeignKey('QuestionGroup')
	form_chatter = models.TextField(help_text='Optional text specific to this respondent that will appear before the form questions.', blank=True)
	display_chatter = models.TextField(help_text='Optional text the reader sees before reading respondent\'s answers.', blank=True)
	contacted = models.BooleanField(default=False, help_text='When respondent has been contacted, check this box.')
	receipt_confirmed = models.BooleanField(default=False, help_text='When respondent has confirmed receipt, check this box.')
	survey_complete = models.BooleanField(default=False, editable=False, help_text='Has the respondent answered the questions currently assigned.')
	confirmation_sent = models.BooleanField(default=False, help_text='Check this after you have sent an email to respondents with their answers.')
	form_slug = models.SlugField(editable=False, unique=True, default='')
	display_slug = models.SlugField(editable=False, unique=True, default='')
	short_url = models.URLField(editable=False, blank=True)
	contact_notes = models.TextField(blank=True, help_text='Type notes on attempts to conduct this assignment here.')

	def contribs(self):
		contribs = []
		for c in self.survey.contributiontypes.all():
			try:
				contribs.append((c, self.contributions.get(contrib_type=c),))
			except Contribution.DoesNotExist:
				contribs.append((c,))
		return contribs

	class Meta:
		unique_together = (('survey', 'respondent'),)
		ordering = ['survey', 'respondent']

	def __unicode__(self):
		return self.respondent.first_name + ' ' + self.respondent.last_name + ' - ' + self.survey.name  
		
	@models.permalink
	def get_absolute_url(self, *args, **kwargs):
		return ('assignment_detail', [self.survey.home_slug, self.display_slug], {},)

	def get_next_profile(self):
		# Get Assignments for this assignment's survey
		assignments = Assignment.objects.filter(survey=self.survey).order_by(
			'-survey_complete', 'respondent__title__order', 'respondent__last_name', 'id')
		
		# Get this assignment's place in the queryset
		self_place = list(assignments.values_list('id', flat=True)).index(self.id)
		
		# If this isn't the last assignment in the queryset, get next assignment...
		if self_place < (assignments.count() - 1):
			return assignments[self_place + 1]
		else:
			return None
			
	def get_prior_profile(self):
		# Get Assignments for this assignment's survey
		assignments = Assignment.objects.filter(survey=self.survey).order_by(
			'-survey_complete', 'respondent__title__order', 'respondent__last_name', 'id')

		# Get this assignment's place in the queryset
		self_place = list(assignments.values_list('id', flat=True)).index(self.id)

		# If this isn't the first assignment, get prior assignment...
		if self_place > 0:
			return assignments[self_place - 1]
		else:
			return None
	
	def tmpl(self):
		txt = "complete" if self.survey_complete else "incomplete"
		return select_template(["%s/survey-%s-text.html" % (self.survey.home_slug, txt), "checkup/survey-%s-text.html" % txt]).name
		
	def save(self, *args, **kwargs):
		super(Assignment, self).save(*args, **kwargs)

		complete_check = (list(self.questions.questions.all().order_by('id').values_list('id', flat=True))
			== list(self.answers.all().order_by('question__question__id').values_list('question__question__id', flat=True))
			and Comment.objects.filter(assignment=self).exists())

		if (complete_check and not self.survey_complete):
			self.survey_complete = True
			self.save()
		elif (not complete_check and self.survey_complete):
			self.survey_complete = False
			self.save()

		not_slugified = str(self.id) + ' ' + self.respondent.first_name + ' '
		not_slugified += self.respondent.last_name
		slugified = slugify(not_slugified)

		if self.display_slug != slugified:
			self.display_slug = slugified
			self.save()

		if self.form_slug == '':
			random_extension = hex(random.randint(10000000, 99999999))
			self.form_slug = str(self.id) + '-' + str(random_extension)
			self.save()

class Answer(models.Model):
	assignment = models.ForeignKey('Assignment', related_name='answers')
	question = models.ForeignKey('QuestionGroupOrder')
	answer = models.ForeignKey('Choice')
	
	class Meta:
		ordering = ['assignment','question__order']
		unique_together = (('assignment', 'question'),)

	def __unicode__(self):
		return '(' + self.assignment.survey.name + ') ' + self.assignment.respondent.last_name + ' - ' + self.question.question.question

class Comment(models.Model):
	assignment = models.OneToOneField('Assignment', primary_key=True, related_name='comment')
	comment = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.assignment.respondent.last_name + ': ' + self.comment


class ContributionType(models.Model):
	survey = models.ForeignKey("Survey", related_name="contributiontypes", blank=True, null=True)
	label = models.CharField(max_length=255)
	contrib_desc = models.CharField(max_length=500, blank=True)
	contrib_footnote = models.CharField(max_length=500, blank=True)
	
	def __unicode__(self):
		return self.label


class Contribution(models.Model):
	contrib_type = models.ForeignKey("ContributionType")
	assignment = models.ForeignKey('Assignment', related_name="contributions")
	contrib_count = models.IntegerField()
	years = models.CharField(max_length=255)
	amount = models.DecimalField(max_digits=12, decimal_places=2)

	def __unicode__(self):
		return self.assignment.respondent.last_name + ' - ' + self.assignment.survey.__unicode__() + ': $' + str(self.amount)


class FormRequest(models.Model):
	key = models.CharField(max_length=50, unique=True)
	assignment = models.ForeignKey('Assignment')
	ip_address = models.IPAddressField()
	request_time = models.DateTimeField(auto_now_add=True)
	page_loaded = models.IntegerField(default=0)
	referer = models.CharField(max_length=255, default='', blank=True)
	user_agent = models.CharField(max_length=255, default='', blank=True)
	
	def __unicode__(self):
		return unicode(self.assignment) + ' - ' + self.request_time.ctime()
		

@receiver(post_delete, sender=Answer, dispatch_uid='answer_delete')
def update_survey_complete_after_answer_delete(sender, **kwargs):
	if 'instance' in kwargs:
		try:
			assignment = kwargs['instance'].assignment
			assignment.save()
		except Assignment.DoesNotExist:
			pass

@receiver(post_delete, sender=Comment, dispatch_uid='comment_delete')
def update_survey_complete_after_comment_delete(sender, **kwargs):
	if 'instance' in kwargs:
		try:
			assignment = kwargs['instance'].assignment
			assignment.save()
		except Assignment.DoesNotExist:
			pass
