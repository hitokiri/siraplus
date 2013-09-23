from django.db import models

class Productos(models.Model):
	nombre 				= models.CharField(max_length=50)
	descripcion 		= models.TextField()
	cantidad 			= models.DecimalField(max_digits=5, decimal_places=2)
	precio 				= models.DecimalField(max_digits=5, decimal_places=2)
	fecha_compra 		= models.DateField()
	fecha_vencimiento  	= models.DateField()
	codigo  			= models.CharField(max_length=50)

	class Meta:
		verbose_name=u'Productos'
		verbose_name_plural = u'Productos'
		ordering = ('fecha_compra',)

	def __unicode__(self):
		return nombre
