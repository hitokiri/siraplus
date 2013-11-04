from django.db import models
from django.contrib.auth.models import User
import datetime


#tipo de cliente para asignarle productos que puede llevar
class TipoCliente(models.Model):
	usuario						= models.ForeignKey(User)
	nombre 						= models.CharField(max_length=150)
	descripcion 				= models.TextField()
	fecha 						= models.DateField(auto_now_add = True)
	codigo 						= models.CharField( max_length=50)

	class Meta:
		verbose_name = ('TipoCliente')
		verbose_name_plural = ('TipoClientes')

	def __unicode__(self):
		return self.nombre

def update_filename(instance, filename):
	    format = "fotografias/" + str(instance.nombres).replace(" ","_")+'/' + str(instance.apellidos).replace(" ", "_") + str(filename[-4: len(filename)])
	    return  format

class Cliente(models.Model):
	GRUPO = ((u'A', 'A'),(u'B', 'B'),(u'C', 'C'),(u'D', 'D'),)
	usuario						= models.ForeignKey(User)
	tipo 						= models.ForeignKey(TipoCliente)
	nombres						= models.CharField('Nombre completo', max_length = 150)
	apellidos					= models.CharField('Apellidos completos' , max_length = 150)
	fecha_naciemiento 			= models.DateField()
	dui 						= models.CharField('Dui', max_length = 10)
	direccion					= models.TextField('Direccion', max_length = 250)
	telefono					= models.CharField('Telefono', max_length = 9)
	fecha_contratacion			= models.DateField('fecha de contratacion')
	activo						= models.BooleanField('Esta activo el trabajador?', default=True)
	contacto_e					= models.CharField('Contacto de emergencia', max_length = 150)
	contacto_e_t				= models.CharField('telefono de contacto', max_length = 9)
	fotografia					= models.ImageField(upload_to = update_filename)
	fecha 						= models.DateField(auto_now_add = True)#cuando se crea el registro
	grupo 						= models.CharField(max_length=10, choices=GRUPO, default = 'A')
	class Meta:
		verbose_name = ('Cliente')
        verbose_name_plural = ('Clientes')

	def __unicode__(self):
		return self.nombres


class Producto(models.Model):
	usuario						= models.ForeignKey(User)
	nombre 						= models.CharField(max_length = 100)
	precio 						= models.DecimalField( decimal_places = 2, max_digits = 5)
	codigo 						= models.CharField(max_length = 150)
	fecha_caducidad 			= models.DateField()
	fecha_compra 				= models.DateField()
	precio_compra 				= models.DecimalField(decimal_places = 2, max_digits = 5)
	producido 					= models.BooleanField()
	cantidad 					= models.DecimalField( decimal_places = 2, max_digits = 5)
	imagen 						= models.ImageField(upload_to= 'productos/')
	fecha 						= models.DateField(auto_now_add = True)

	class Meta:
		verbose_name = ('Producto')
		verbose_name_plural = ('Productos')

	def __unicode__(self):
		return self.nombre



#Encargada de llevar los prestamos no relacionados con la mercancia
class Prestamo(models.Model):
	usuario						= models.ForeignKey(User)
	cliente						= models.ForeignKey(Cliente, blank=True, null=True)
	nocliente 					= models.CharField(max_length=150, null=True, blank=True)
	concepto 					= models.CharField(max_length=100)
	descripcion 				= models.CharField(max_length=150)
	cantidad 					= models.DecimalField(max_digits=5, decimal_places=2)
	fecha 						= models.DateField(auto_now_add = True)

	class Meta:
		verbose_name = ('Prestamo')
		verbose_name_plural = ('Prestamos')

	def __unicode__(self):
		if self.cliente:
			nombre = str(self.cliente)
		else:
			nombre = str(self.nocliente)
		return nombre

#esta parte lleva las deudas de los TipoClientes MasterDeusaPedidoPagoMasoMenos
class MasterDPPA(models.Model):
	GRUPO = ((u'A', 'A'),(u'B', 'B'),(u'C', 'C'),(u'D', 'D'),)
	CHOICE_TIPO = ((2,'Deuda'),(3,'Pedido'),(1,'Pago'),(4, 'entrega'),)
	usuario						= models.ForeignKey(User)
	tipo 						= models.IntegerField(choices= CHOICE_TIPO)
	basado_en 					= models.ForeignKey('MasterDPPA', blank=True, null=True, related_name='basado') # este campo especifica de que pedido es  el pago
	cliente 					= models.ForeignKey(Cliente)
	total						= models.DecimalField(decimal_places = 2, max_digits = 5, blank=True, null=True)
	fecha_entrega 				= models.DateField(default = datetime.date.today()- datetime.timedelta(-1), blank=True, null=True)
	fecha 						= models.DateField(auto_now_add = True)
	tiene_modificaciones 		= models.BooleanField()
	es_modificacion_de 			= models.ForeignKey('MasterDPPA', blank=True, null=True)
	pago_f_v					= models.BooleanField()
	grupo 						= models.CharField(max_length=10, choices=GRUPO, default='A')
	entregado 					= models.BooleanField()


	class Meta:
		verbose_name = ('MasterDPPA')
		verbose_name_plural = ('MasterDPPA')

	def __unicode__(self):
		return  '%s - %d' % (self.cliente,self.tipo)
#cada uno de los productos que conforman MasterDeusaPedidoPagoAbono
class ProductoDPPA(models.Model):
	usuario						= models.ForeignKey(User)
	tipo						= models.ForeignKey(MasterDPPA)
	producto 					= models.ForeignKey('Producto')
	cantidad 					= models.DecimalField( decimal_places = 2, max_digits = 5, default = 0)
	precios 					= models.DecimalField( decimal_places = 2, max_digits = 5, default = 0)
	fecha 						= models.DateField(auto_now_add = True)
	cambios 		 			= models.DecimalField(max_digits=5, decimal_places=2, default = 0, null=True, blank=True)#este campo guarda los cambios de cantidades de mas o menos  en el producto de el pedido
	compenzacion_can 			= models.DecimalField(max_digits=5, decimal_places=2, default=0)
	compenzacion_tipo 			= models.CharField(max_length=3, default='')

	class Meta:
		verbose_name = ('ProductoDPPA')
		verbose_name_plural = ('ProductoDPPA')

	def __unicode__(self):
		return  '%s - %s' % (str(self.tipo),str(self.producto))