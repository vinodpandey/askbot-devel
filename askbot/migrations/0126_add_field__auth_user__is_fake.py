# encoding: utf-8
from askbot.compat import AUTH_USER_MODEL, auth_db_name
from south.db import db
from south.v2 import SchemaMigration
from askbot.migrations_api import safe_add_column

class Migration(SchemaMigration):

    def forwards(self, orm):
        safe_add_column(
            auth_db_name, 'is_fake',
            self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

    def backwards(self, orm):
        db.delete_column(auth_db_name, 'is_fake')

    complete_apps = ['askbot']
