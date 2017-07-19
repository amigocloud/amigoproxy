# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Target'
        db.create_table(u'proxy_target', (
            ('id', self.gf('django.db.models.fields.CharField')(default='d8954ba2f7', max_length=10, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'proxy', ['Target'])

        # Adding model 'Source'
        db.create_table(u'proxy_source', (
            ('id', self.gf('django.db.models.fields.CharField')(default='2ec7bbaba7', max_length=10, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'proxy', ['Source'])

        # Adding model 'Group'
        db.create_table(u'proxy_group', (
            ('id', self.gf('django.db.models.fields.CharField')(default='97989958ee', max_length=10, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'proxy', ['Group'])

        # Adding M2M table for field targets on 'Group'
        m2m_table_name = db.shorten_name(u'proxy_group_targets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'proxy.group'], null=False)),
            ('target', models.ForeignKey(orm[u'proxy.target'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'target_id'])

        # Adding M2M table for field sources on 'Group'
        m2m_table_name = db.shorten_name(u'proxy_group_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'proxy.group'], null=False)),
            ('source', models.ForeignKey(orm[u'proxy.source'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'source_id'])


    def backwards(self, orm):
        # Deleting model 'Target'
        db.delete_table(u'proxy_target')

        # Deleting model 'Source'
        db.delete_table(u'proxy_source')

        # Deleting model 'Group'
        db.delete_table(u'proxy_group')

        # Removing M2M table for field targets on 'Group'
        db.delete_table(db.shorten_name(u'proxy_group_targets'))

        # Removing M2M table for field sources on 'Group'
        db.delete_table(db.shorten_name(u'proxy_group_sources'))


    models = {
        u'proxy.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'c6844907b6'", 'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': u"orm['proxy.Source']"}),
            'targets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': u"orm['proxy.Target']"})
        },
        u'proxy.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.CharField', [], {'default': "'72edd8ec08'", 'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'proxy.target': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Target'},
            'id': ('django.db.models.fields.CharField', [], {'default': "'2d27d9b5e6'", 'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['proxy']