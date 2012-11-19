# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Character'
        db.create_table('piece_character', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('age', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('piece', ['Character'])

        # Adding model 'Event'
        db.create_table('piece_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('piece', ['Event'])

        # Adding M2M table for field characters on 'Event'
        db.create_table('piece_event_characters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['piece.event'], null=False)),
            ('character', models.ForeignKey(orm['piece.character'], null=False))
        ))
        db.create_unique('piece_event_characters', ['event_id', 'character_id'])

        # Adding model 'Piece'
        db.create_table('piece_piece', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('piece', ['Piece'])

        # Adding M2M table for field events on 'Piece'
        db.create_table('piece_piece_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('piece', models.ForeignKey(orm['piece.piece'], null=False)),
            ('event', models.ForeignKey(orm['piece.event'], null=False))
        ))
        db.create_unique('piece_piece_events', ['piece_id', 'event_id'])

        # Adding M2M table for field characters on 'Piece'
        db.create_table('piece_piece_characters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('piece', models.ForeignKey(orm['piece.piece'], null=False)),
            ('character', models.ForeignKey(orm['piece.character'], null=False))
        ))
        db.create_unique('piece_piece_characters', ['piece_id', 'character_id'])


    def backwards(self, orm):
        # Deleting model 'Character'
        db.delete_table('piece_character')

        # Deleting model 'Event'
        db.delete_table('piece_event')

        # Removing M2M table for field characters on 'Event'
        db.delete_table('piece_event_characters')

        # Deleting model 'Piece'
        db.delete_table('piece_piece')

        # Removing M2M table for field events on 'Piece'
        db.delete_table('piece_piece_events')

        # Removing M2M table for field characters on 'Piece'
        db.delete_table('piece_piece_characters')


    models = {
        'piece.character': {
            'Meta': {'object_name': 'Character'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
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