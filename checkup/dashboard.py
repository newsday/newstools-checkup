"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'checkups.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
		
        self.children.append(modules.ModelList(
            _('CheckUp:  First, add a survey and respondents...'),
            column=1,
            collapsible=False,
            models=('checkup.models.Survey', 'checkup.models.Respondent',),
        ))

        self.children.append(modules.ModelList(
            _('CheckUp:  Then, create groups of questions...'),
            column=1,
            collapsible=False,
            models=('checkup.models.QuestionGroup',),
        ))
		
        self.children.append(modules.ModelList(
            _('CheckUp:  Finally, create assignments that tie everything together...'),
            column=1,
            collapsible=False,
            models=('checkup.models.Assignment',),
        ))
		
        self.children.append(modules.ModelList(
            _('CheckUp:  You can also add political contribution data to respondents...'),
            column=1,
            collapsible=False,
            models=('checkup.models.ContributionType',
                    'checkup.models.Contribution',),
        ))
		
        self.children.append(modules.ModelList(
            _('CheckUp:  Modify other elements individually here...'),
            column=1,
            collapsible=False,
            models=('checkup.models.Question', 'checkup.models.Group', 
					'checkup.models.Title', 'checkup.models.Choice', 'checkup.models.ChoiceDisplay',
					'checkup.models.Answer', 'checkup.models.Comment',),
        ))
		
        self.children.append(modules.ModelList(
            _('Administration'),
            column=3,
            collapsible=False,
            models=('django.contrib.*', 'checkup.models.Reporter',
					'checkup.models.FormRequest', 'dbtemplates.models.Template'),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=3,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Google-Code'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
            ]
        ))
		
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


