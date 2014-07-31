# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PostTaggedItem'
        db.create_table(u'site_core_posttaggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'site_core_posttaggeditem_items', to=orm['taggit.Tag'])),
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site_core.Post'])),
        ))
        db.send_create_signal(u'site_core', ['PostTaggedItem'])

        # Adding model 'Post'
        db.create_table(u'site_core_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('body', self.gf('ckeditor.fields.RichTextField')()),
            ('body_split', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('read_more', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('categories', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site_core.Category'])),
            ('slug', self.gf('django.db.models.fields.CharField')(default=None, max_length=512, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default=None, max_length=512, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(default=None, max_length=512, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('attached', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'site_core', ['Post'])

        # Adding model 'Page'
        db.create_table(u'site_core_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('body', self.gf('ckeditor.fields.RichTextField')()),
            ('parent_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site_core.Page'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(default=None, max_length=512, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default=None, max_length=512, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(default=None, max_length=512, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('in_menu', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'site_core', ['Page'])

        # Adding model 'Category'
        db.create_table(u'site_core_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=512)),
            ('slug', self.gf('django.db.models.fields.CharField')(default=None, max_length=512, null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
        ))
        db.send_create_signal(u'site_core', ['Category'])

        # Adding model 'Parameter'
        db.create_table(u'site_core_parameter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'site_core', ['Parameter'])


    def backwards(self, orm):
        # Deleting model 'PostTaggedItem'
        db.delete_table(u'site_core_posttaggeditem')

        # Deleting model 'Post'
        db.delete_table(u'site_core_post')

        # Deleting model 'Page'
        db.delete_table(u'site_core_page')

        # Deleting model 'Category'
        db.delete_table(u'site_core_category')

        # Deleting model 'Parameter'
        db.delete_table(u'site_core_parameter')


    models = {
        u'site_core.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'site_core.page': {
            'Meta': {'object_name': 'Page'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'body': ('ckeditor.fields.RichTextField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512', 'blank': 'True'}),
            'parent_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site_core.Page']", 'null': 'True', 'blank': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'site_core.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        u'site_core.post': {
            'Meta': {'object_name': 'Post'},
            'attached': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'body': ('ckeditor.fields.RichTextField', [], {}),
            'body_split': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site_core.Category']"}),
            'description': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512', 'blank': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'read_more': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'site_core.posttaggeditem': {
            'Meta': {'object_name': 'PostTaggedItem'},
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site_core.Post']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'site_core_posttaggeditem_items'", 'to': u"orm['taggit.Tag']"})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['site_core']