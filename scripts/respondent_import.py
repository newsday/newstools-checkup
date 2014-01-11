import csv
import os
import argparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "checkups.settings")

from checkup.models import Respondent, Group, Title, Survey, QuestionGroup, Reporter, Assignment

def main():
	
	##############################
	## Set up command line tool ##
	##############################
	
	parser = argparse.ArgumentParser(
			description='Import respondents into CheckUp.',
			epilog='Importer written by Matt Clark an Adam Playford.')

	parser.add_argument('file', help='The CSV file to be imported.')
	parser.add_argument('survey_slug', help='The slug of the survey to import data to.')

	args = parser.parse_args()

	try:
		survey = Survey.objects.get(home_slug=args.survey_slug)
	except Survey.DoesNotExist:
		print('Could not find a Survey with slug "%s"' % args.survey_slug)
		return
	
	with open(args.file, 'rU') as csvfile:
		respondents = csv.DictReader(csvfile)
		
		for row in respondents:
			############################
			## Create each respondant ##
			############################
			
			group, group_created = Group.objects.get_or_create(name=row['group'])
			
			try:
				respondent = Respondent.objects.get(sheet_id=int(row['sheet_id']))
			except(Respondent.DoesNotExist):
				respondent = Respondent(sheet_id=int(row['sheet_id']))
			
			# Set columns that will auto-populate from the csv
			cols = [
				'party', 'district', 'gender', 'first_name', 'last_name',
				'website', 'office_phone', 'email', 'twitter', 'address',
				'address2', 'city', 'state', 'zip', 'headshot'
			]
			
			# Get values out of databases
			try:
				title = Title.objects.get(long=row['long'])
				title.short, title.order = row['short'], row['order']
				title.save()
			except Title.DoesNotExist:
				title = Title.objects.create(long=row['long'], short=row['short'], order=row['order'])
			except Title.MultipleObjectsReturned:
				Title.objects.filter(long=row['long']).delete()
				title = Title.objects.create(long=row['long'], short=row['short'], order=row['order'])
			
			# set values
			for col in cols:
				setattr(respondent, col, row[col])
			respondent.group, respondent.title = group, title
			respondent.save()
			
			# Create or update assignment
			
			# Auto-populate columns
			assignment_cols = ['form_chatter', 'display_chatter']
			
			# From the database
			try:
				reporter = Reporter.objects.get(user__last_name=row['reporter'])
			except Reporter.DoesNotExist:
				print('Error! Reporter with last name "%s" not in database.' % row['reporter'])
				return
			
			try:
				assignment = respondent.assignments.get(survey=survey)
			except Assignment.DoesNotExist:
				assignment = Assignment(survey=survey, respondent=respondent)
			
			assignment.questions = QuestionGroup.objects.get(name=row['question_group'])
			assignment.reporter = reporter
			for col in assignment_cols:
				setattr(assignment, col, row[col])
			assignment.save()
			
if __name__=="__main__":
	main()