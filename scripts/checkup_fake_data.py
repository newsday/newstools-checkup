import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "checkups.settings")

from checkup.models import Assignment, Answer, Comment, Question, QuestionGroup, QuestionGroupOrder

delete_stuff = raw_input('Delete Answers and comments before generating ("Y/N")')
if delete_stuff == 'Y':
	Answer.objects.all().delete()
	Comment.objects.all().delete()

answer_questions = random.randint(1,3)

for assign in Assignment.objects.filter(survey_complete=False):
	if answer_questions == 1:
		qs = assign.questions.questions.all()
		for q in qs:
			choices = q.choices.all()
			choice = random.choice(choices)
			
			group = assign.questions
			group_order = QuestionGroupOrder.objects.get(
							question=q, group=group)

			answer = Answer.objects.get_or_create(assignment=assign, 
						question=group_order, 
						answer=choice)
		
		new_comment = 'Here is a comment. Here is a comment. Here is a comment.'
		comment = Comment.objects.get_or_create(assignment=assign,
			comment=new_comment)

		assign.survey_complete = True
		assign.save()
	else:
		pass
	
	answer_questions = random.randint(1,3)