# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Owner.photo'
        db.add_column(u'contact_owner', 'photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Owner.photo'
        db.delete_column(u'contact_owner', 'photo')


    models = {
        u'contact.owner': {
            'Meta': {'object_name': 'Owner'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'birthday': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'other_into': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'contact.usersrequest': {
            'Meta': {'object_name': 'UsersRequest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_str': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['contact']