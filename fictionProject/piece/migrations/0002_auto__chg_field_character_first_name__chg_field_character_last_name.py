# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Character.first_name'
        db.alter_column('piece_character', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Character.last_name'
        db.alter_column('piece_character', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

    def backwards(self, orm):

        # Changing field 'Character.first_name'
        db.alter_column('piece_character', 'first_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

        # Changing field 'Character.last_name'
        db.alter_column('piece_character', 'last_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=30))

    models = {
        'piece.character': {
            'Meta': {'object_name': 'Character'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'piece.event': {
            'Meta': {'object_name': 'Event'},
            'characters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['piece.Character']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'piece.piece': {
            'Meta': {'object_name': 'Piece'},
            'characters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['piece.Character']", 'null': 'True', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['piece.Event']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['piece']