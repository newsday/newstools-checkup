# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.order'
        db.add_column(u'checkup_question', 'order',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.order'
        db.delete_column(u'checkup_question', 'order')


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
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
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