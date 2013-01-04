# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Character'
        db.create_table('subject_character', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('age', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('eye_color', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('subject', ['Character'])


    def backwards(self, orm):
        # Deleting model 'Character'
        db.delete_table('subject_character')


    models = {
        'subject.character': {
            'Meta': {'object_name': 'Character'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'eye_color': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['subject']