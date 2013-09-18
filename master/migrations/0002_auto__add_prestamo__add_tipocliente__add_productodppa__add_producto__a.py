# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Prestamo'
        db.create_table(u'master_prestamo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['master.Cliente'], null=True, blank=True)),
            ('nocliente', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('concepto', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('cantidad', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'master', ['Prestamo'])

        # Adding model 'TipoCliente'
        db.create_table(u'master_tipocliente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'master', ['TipoCliente'])

        # Adding model 'ProductoDPPA'
        db.create_table(u'master_productodppa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['master.MasterDPPA'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['master.Producto'])),
            ('cantidad', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('precios', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'master', ['ProductoDPPA'])

        # Adding model 'Producto'
        db.create_table(u'master_producto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('precio', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('fecha_caducidad', self.gf('django.db.models.fields.DateField')()),
            ('fecha_compra', self.gf('django.db.models.fields.DateField')()),
            ('precio_compra', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('producido', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cantidad', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'master', ['Producto'])

        # Adding model 'Cliente'
        db.create_table(u'master_cliente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['master.TipoCliente'])),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('dui', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('direccion', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contacto_e', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('contacto_e_t', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('fotografia', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'master', ['Cliente'])

        # Adding model 'MasterDPPA'
        db.create_table(u'master_masterdppa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
            ('basado_en', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['master.Cliente'])),
            ('total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('fecha_entrega', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 6, 24, 0, 0))),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'master', ['MasterDPPA'])


    def backwards(self, orm):
        # Deleting model 'Prestamo'
        db.delete_table(u'master_prestamo')

        # Deleting model 'TipoCliente'
        db.delete_table(u'master_tipocliente')

        # Deleting model 'ProductoDPPA'
        db.delete_table(u'master_productodppa')

        # Deleting model 'Producto'
        db.delete_table(u'master_producto')

        # Deleting model 'Cliente'
        db.delete_table(u'master_cliente')

        # Deleting model 'MasterDPPA'
        db.delete_table(u'master_masterdppa')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'master.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'contacto_e': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'contacto_e_t': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'direccion': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'dui': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fotografia': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['master.TipoCliente']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'master.masterdppa': {
            'Meta': {'object_name': 'MasterDPPA'},
            'basado_en': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['master.Cliente']"}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_entrega': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 6, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {}),
            'total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'master.prestamo': {
            'Meta': {'object_name': 'Prestamo'},
            'cantidad': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['master.Cliente']", 'null': 'True', 'blank': 'True'}),
            'concepto': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nocliente': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'master.producto': {
            'Meta': {'object_name': 'Producto'},
            'cantidad': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_caducidad': ('django.db.models.fields.DateField', [], {}),
            'fecha_compra': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'precio_compra': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'producido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'master.productodppa': {
            'Meta': {'object_name': 'ProductoDPPA'},
            'cantidad': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precios': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['master.Producto']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['master.MasterDPPA']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'master.tipocliente': {
            'Meta': {'object_name': 'TipoCliente'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['master']