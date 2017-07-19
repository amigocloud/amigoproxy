# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Target.reverse'
        db.add_column(u'proxy_target', 'reverse',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Target.response_format'
        db.add_column(u'proxy_target', 'response_format',
                      self.gf('django.db.models.fields.CharField')(default='xml', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Target.reverse'
        db.delete_column(u'proxy_target', 'reverse')

        # Deleting field 'Target.response_format'
        db.delete_column(u'proxy_target', 'response_format')


    models = {
        u'proxy.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'f364da9314'", 'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': u"orm['proxy.Source']"}),
            'targets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': u"orm['proxy.Target']"})
        },
        u'proxy.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.CharField', [], {'default': "'3fc06bbc19'", 'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'proxy.target': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Target'},
            'id': ('django.db.models.fields.CharField', [], {'default': "'542d9976ff'", 'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'response_format': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reverse': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['proxy']