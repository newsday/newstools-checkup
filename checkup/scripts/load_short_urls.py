import os
import argparse

from urllib2 import urlopen

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "checkups.settings")

from django.conf import settings
from django.contrib.sites.models import Site
from checkup.models import Survey, Assignment

def get_short_url(long_url):
	bitly_url = ('https://api-ssl.bitly.com/v3/shorten?access_token=%s&longUrl=%s&format=txt' % (
		settings.BITLY_OAUTH2, long_url))
	return urlopen(bitly_url).read()[:-1]
	

def main():
	##############################
	## Set up command line tool ##
	##############################
	
	parser = argparse.ArgumentParser(
			description='Create short links for assignments if they don\'t exist.',
			epilog='Script written by Matt Clark.')

	parser.add_argument('survey_slug', help='The slug of the survey to create short URLs for.')
	
	url_domain_help = 'Specify a different domain then the default, which is "' + Site.objects.get_current().domain + '."'
	url_path_help = 'Specify initial path (before survey and assignment slugs) then the default, '
	url_path_help += 'which is "/checkup/." Include initial and trailing slashes.'
	
	parser.add_argument("-d", "--url_domain", help=url_domain_help, default=Site.objects.get_current().domain)
	parser.add_argument("-p", "--url_path", help=url_path_help, default='/checkup/')

	args = parser.parse_args()
	
	try:
		survey = Survey.objects.get(home_slug=args.survey_slug)
	except Survey.DoesNotExist:
		print('Could not find a Survey with slug "%s"' % args.survey_slug)
		return
		
	counter = 0
		
	for assign in Assignment.objects.filter(survey=survey):
		display_url = 'http://' + args.url_domain + args.url_path
		display_url += survey.home_slug + '/' + assign.display_slug + '/'
		
		short_url = get_short_url(display_url)
		
		assign.short_url = short_url
		assign.save()
		counter += 1
		
	print 'Saved ' + str(counter) + ' short urls that start with: http://' + args.url_domain + args.url_path

if __name__=="__main__":
	main()