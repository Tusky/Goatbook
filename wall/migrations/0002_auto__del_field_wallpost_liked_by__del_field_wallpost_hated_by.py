# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'WallPost.liked_by'
        db.delete_column('wall_wallpost', 'liked_by_id')

        # Deleting field 'WallPost.hated_by'
        db.delete_column('wall_wallpost', 'hated_by_id')

        # Adding M2M table for field liked_by on 'WallPost'
        db.create_table('wall_wallpost_liked_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wallpost', models.ForeignKey(orm['wall.wallpost'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('wall_wallpost_liked_by', ['wallpost_id', 'user_id'])

        # Adding M2M table for field hated_by on 'WallPost'
        db.create_table('wall_wallpost_hated_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wallpost', models.ForeignKey(orm['wall.wallpost'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('wall_wallpost_hated_by', ['wallpost_id', 'user_id'])


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'WallPost.liked_by'
        raise RuntimeError("Cannot reverse this migration. 'WallPost.liked_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'WallPost.hated_by'
        raise RuntimeError("Cannot reverse this migration. 'WallPost.hated_by' and its values cannot be restored.")
        # Removing M2M table for field liked_by on 'WallPost'
        db.delete_table('wall_wallpost_liked_by')

        # Removing M2M table for field hated_by on 'WallPost'
        db.delete_table('wall_wallpost_hated_by')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'wall.wallpost': {
            'Meta': {'object_name': 'WallPost'},
            'hated_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hated by'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liked_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'liked by'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'post': ('django.db.models.fields.TextField', [], {}),
            'posted_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'poster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poster'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['wall']