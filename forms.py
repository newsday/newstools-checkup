from django import forms
from django.contrib.auth.models import User


class SurveyForm(forms.Form):
		
	def __init__(self, *args, **kwargs):
		assignment = kwargs.pop('assignment')
		super(SurveyForm, self).__init__(*args, **kwargs)
		
		questions = assignment.questions.questions.all().order_by('questiongrouporder__order')
		
		for question in questions:
			choices = []
			for choice in question.choices.all():
				choices.append((choice.id, choice.choice))

			self.fields['question-%s' % question.id] = forms.ChoiceField(
				widget=forms.RadioSelect(), 
				choices=choices, label=question.question,
				help_text=question.explanation)
		
		self.fields['comment'] = forms.CharField(max_length=30000, required=False,
				widget=forms.Textarea(attrs={'rows': 11, 'class': 'form-control'}))
				
		authorized_label = 'I am ' + ' ' + assignment.respondent.title.short
		authorized_label += ' ' + assignment.respondent.first_name
		authorized_label += ' ' + assignment.respondent.last_name + ' or someone authorized to '
		authorized_label += 'submit this form on their behalf. I understand that my access to '
		authorized_label += 'this form has been logged for security purposes.'
	
		self.fields['authorized'] = forms.BooleanField(label=authorized_label)