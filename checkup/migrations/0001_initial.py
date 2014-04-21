# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Reporter'
        db.create_table(u'checkup_reporter', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.Title'], blank=True)),
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'checkup', ['Reporter'])

        # Adding model 'Survey'
        db.create_table(u'checkup_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('form_chatter', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('home_slug', self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=50)),
            ('display_chatter', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('display_byline', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'checkup', ['Survey'])

        # Adding model 'Group'
        db.create_table(u'checkup_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75)),
        ))
        db.send_create_signal(u'checkup', ['Group'])

        # Adding model 'Title'
        db.create_table(u'checkup_title', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('long', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'checkup', ['Title'])

        # Adding unique constraint on 'Title', fields ['short', 'long']
        db.create_unique(u'checkup_title', ['short', 'long'])

        # Adding model 'Respondent'
        db.create_table(u'checkup_respondent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.Group'])),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.Title'])),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=254, blank=True)),
            ('office_phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('state', self.gf('localflavor.us.models.USPostalCodeField')(max_length=2, blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('headshot', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('contact_phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('sheet_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'checkup', ['Respondent'])

        # Adding model 'Question'
        db.create_table(u'checkup_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('explanation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('directed_to', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('visualize', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'checkup', ['Question'])

        # Adding M2M table for field choices on 'Question'
        m2m_table_name = db.shorten_name(u'checkup_question_choices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'checkup.question'], null=False)),
            ('choice', models.ForeignKey(orm[u'checkup.choice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'choice_id'])

        # Adding model 'ChoiceDisplay'
        db.create_table(u'checkup_choicedisplay', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('display', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('no_answer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal(u'checkup', ['ChoiceDisplay'])

        # Adding model 'Choice'
        db.create_table(u'checkup_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.ChoiceDisplay'])),
            ('choice', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75)),
        ))
        db.send_create_signal(u'checkup', ['Choice'])

        # Adding model 'QuestionGroup'
        db.create_table(u'checkup_questiongroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75)),
        ))
        db.send_create_signal(u'checkup', ['QuestionGroup'])

        # Adding model 'QuestionGroupOrder'
        db.create_table(u'checkup_questiongrouporder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.QuestionGroup'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.Question'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'checkup', ['QuestionGroupOrder'])

        # Adding model 'Assignment'
        db.create_table(u'checkup_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments', to=orm['checkup.Survey'])),
            ('respondent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments', to=orm['checkup.Respondent'])),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.Reporter'], blank=True)),
            ('questions', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.QuestionGroup'])),
            ('form_chatter', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('display_chatter', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contacted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('receipt_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('survey_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('confirmation_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('form_slug', self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=50)),
            ('display_slug', self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=50)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('contact_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'checkup', ['Assignment'])

        # Adding unique constraint on 'Assignment', fields ['survey', 'respondent']
        db.create_unique(u'checkup_assignment', ['survey_id', 'respondent_id'])

        # Adding model 'Answer'
        db.create_table(u'checkup_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['checkup.Assignment'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.QuestionGroupOrder'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.Choice'])),
        ))
        db.send_create_signal(u'checkup', ['Answer'])

        # Adding unique constraint on 'Answer', fields ['assignment', 'question']
        db.create_unique(u'checkup_answer', ['assignment_id', 'question_id'])

        # Adding model 'Comment'
        db.create_table(u'checkup_comment', (
            ('assignment', self.gf('django.db.models.fields.related.OneToOneField')(related_name='comment', unique=True, primary_key=True, to=orm['checkup.Assignment'])),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'checkup', ['Comment'])

        # Adding model 'ContributionType'
        db.create_table(u'checkup_contributiontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='contributiontypes', null=True, to=orm['checkup.Survey'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contrib_desc', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('contrib_footnote', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'checkup', ['ContributionType'])

        # Adding model 'Contribution'
        db.create_table(u'checkup_contribution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contrib_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.ContributionType'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contributions', to=orm['checkup.Assignment'])),
            ('contrib_count', self.gf('django.db.models.fields.IntegerField')()),
            ('years', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'checkup', ['Contribution'])

        # Adding model 'FormRequest'
        db.create_table(u'checkup_formrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkup.Assignment'])),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('request_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('page_loaded', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('referer', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'checkup', ['FormRequest'])


    def backwards(self, orm):
        # Removing unique constraint on 'Answer', fields ['assignment', 'question']
        db.delete_unique(u'checkup_answer', ['assignment_id', 'question_id'])

        # Removing unique constraint on 'Assignment', fields ['survey', 'respondent']
        db.delete_unique(u'checkup_assignment', ['survey_id', 'respondent_id'])

        # Removing unique constraint on 'Title', fields ['short', 'long']
        db.delete_unique(u'checkup_title', ['short', 'long'])

        # Deleting model 'Reporter'
        db.delete_table(u'checkup_reporter')

        # Deleting model 'Survey'
        db.delete_table(u'checkup_survey')

        # Deleting model 'Group'
        db.delete_table(u'checkup_group')

        # Deleting model 'Title'
        db.delete_table(u'checkup_title')

        # Deleting model 'Respondent'
        db.delete_table(u'checkup_respondent')

        # Deleting model 'Question'
        db.delete_table(u'checkup_question')

        # Removing M2M table for field choices on 'Question'
        db.delete_table(db.shorten_name(u'checkup_question_choices'))

        # Deleting model 'ChoiceDisplay'
        db.delete_table(u'checkup_choicedisplay')

        # Deleting model 'Choice'
        db.delete_table(u'checkup_choice')

        # Deleting model 'QuestionGroup'
        db.delete_table(u'checkup_questiongroup')

        # Deleting model 'QuestionGroupOrder'
        db.delete_table(u'checkup_questiongrouporder')

        # Deleting model 'Assignment'
        db.delete_table(u'checkup_assignment')

        # Deleting model 'Answer'
        db.delete_table(u'checkup_answer')

        # Deleting model 'Comment'
        db.delete_table(u'checkup_comment')

        # Deleting model 'ContributionType'
        db.delete_table(u'checkup_contributiontype')

        # Deleting model 'Contribution'
        db.delete_table(u'checkup_contribution')

        # Deleting model 'FormRequest'
        db.delete_table(u'checkup_formrequest')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'checkup.answer': {
            'Meta': {'ordering': "['assignment', 'question__order']", 'unique_together': "(('assignment', 'question'),)", 'object_name': 'Answer'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.Choice']"}),
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['checkup.Assignment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.QuestionGroupOrder']"})
        },
        u'checkup.assignment': {
            'Meta': {'ordering': "['survey', 'respondent']", 'unique_together': "(('survey', 'respondent'),)", 'object_name': 'Assignment'},
            'confirmation_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contacted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_chatter': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'form_chatter': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'form_slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questions': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.QuestionGroup']"}),
            'receipt_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.Reporter']", 'blank': 'True'}),
            'respondent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['checkup.Respondent']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['checkup.Survey']"}),
            'survey_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'checkup.choice': {
            'Meta': {'ordering': "('-display__order',)", 'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'display': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.ChoiceDisplay']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'checkup.choicedisplay': {
            'Meta': {'object_name': 'ChoiceDisplay'},
            'display': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'checkup.comment': {
            'Meta': {'object_name': 'Comment'},
            'assignment': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'comment'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['checkup.Assignment']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'checkup.contribution': {
            'Meta': {'object_name': 'Contribution'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contributions'", 'to': u"orm['checkup.Assignment']"}),
            'contrib_count': ('django.db.models.fields.IntegerField', [], {}),
            'contrib_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.ContributionType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'years': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'checkup.contributiontype': {
            'Meta': {'object_name': 'ContributionType'},
            'contrib_desc': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'contrib_footnote': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contributiontypes'", 'null': 'True', 'to': u"orm['checkup.Survey']"})
        },
        u'checkup.formrequest': {
            'Meta': {'object_name': 'FormRequest'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.Assignment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'page_loaded': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'referer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'request_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        u'checkup.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'})
        },
        u'checkup.question': {
            'Meta': {'object_name': 'Question'},
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['checkup.Choice']", 'symmetrical': 'False'}),
            'directed_to': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'visualize': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'checkup.questiongroup': {
            'Meta': {'object_name': 'QuestionGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['checkup.Question']", 'through': u"orm['checkup.QuestionGroupOrder']", 'symmetrical': 'False'})
        },
        u'checkup.questiongrouporder': {
            'Meta': {'ordering': "['order']", 'object_name': 'QuestionGroupOrder'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.QuestionGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.Question']"})
        },
        u'checkup.reporter': {
            'Meta': {'object_name': 'Reporter'},
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.Title']", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'checkup.respondent': {
            'Meta': {'ordering': "['title', 'last_name']", 'object_name': 'Respondent'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'contact_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.Group']"}),
            'headshot': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'office_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'sheet_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state': ('localflavor.us.models.USPostalCodeField', [], {'max_length': '2', 'blank': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkup.Title']"}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '254', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        u'checkup.survey': {
            'Meta': {'object_name': 'Survey'},
            'display_byline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_chatter': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'form_chatter': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'home_slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'checkup.title': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('short', 'long'),)", 'object_name': 'Title'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['checkup']