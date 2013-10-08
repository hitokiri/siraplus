#encoding:utf-8
from django.views.decorators.csrf import csrf_protect
from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from master.forms import *
from master.models import  *
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.forms.formsets import formset_factory, BaseFormSet
import datetime
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.forms.models import modelformset_factory, BaseModelFormSet #lo que se necesita para crear moderfolmset https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#using-a-model-formset-in-a-view


def vista_index(request):
	#esta parte recolecta lo de next para hacer la redireccion claro si hay un next
	try:
		meta = request.META['QUERY_STRING'].split('=')[1][:-1]
	except IndexError:
		meta = None
	foot = False
	vista = 'Inicio de Seción'
	error = ""
 	if request.method == 'POST':
 		formulario = LoginForm(request.POST)
 		if formulario.is_valid():
 			usuario = formulario.cleaned_data['usuario']
 			contrasena = formulario.cleaned_data['contrasena']
 			#paso de cotejamiento de el usuario y la contraseña ingresados en el formulario
 			user = authenticate(username = usuario, password = contrasena)
 			if user:
 				if user.is_active:
 					login(request, user)
 					#esta parte redirecciona a la ista de donde fue enviado y si no fue redireccionado para login simplemente manda a pizarra
 					if  meta:
	 					return HttpResponseRedirect(meta)
	 				else:
	 					return HttpResponseRedirect('/pizarra')
	 		else:
	 			#mandamos el error para decir que no es bueno el usuario o la contraseña
	 			error='El usuario o la contraseña son erroneos, Por favor ingrese los datos correctamente'
 	else:
 		formulario = LoginForm()
	ctx ={'nombre_sistema': settings, 'foot': foot, 'vista': vista , 'formulario': formulario, 'error': error}
	return render_to_response('index.html', ctx,context_instance = RequestContext(request))

def logout_vista(request):
	try:
		logout_salir = request.META['HTTP_REFERER'].split('http://'+request.META['HTTP_HOST'])[1][:-1]
		logout(request)
		return HttpResponseRedirect(logout_salir)

	except KeyError:
		return HttpResponseRedirect('/')

@login_required(login_url = '/')
def vista_crear_vendedora(request):
	try:
		request.META['HTTP_REFERER']
	except KeyError:
		return HttpResponseRedirect('/listar/cliente')
	foot = True
	vista = 'Crear Client'
	if request.method == 'POST':
		#sesion 				= User.objects.get(username = request.user.username)
		sesion 				= request.user.id
		formulario 			= VendedoraForm(request.POST, request.FILES)
		if formulario.is_valid():
			cliente 		= formulario.save(commit=False)
			cliente.usuario_id = sesion
			cliente.save()
			#esta parte esta dedicada para la creacion de la deuda
			pedido 			= MasterDPPA(usuario_id=sesion, tipo=2, cliente= cliente, total=0.0)
			pedido.save()
			productos 		= Producto.objects.filter(Q(nombre__startswith ='quesadilla') | Q(nombre__startswith = 'torta')) #sacar los id y los precios de los productos
			for x in productos:
				prod_pedido = ProductoDPPA(usuario_id=sesion, tipo=pedido, producto= x)
				prod_pedido.save()
			return HttpResponseRedirect('/listar/cliente')
	else:
		formulario = VendedoraForm()
	ctx ={'formulario':formulario, 'nombre_sistema': settings, 'foot': foot, 'vista': vista}
	return render_to_response('vendedora.html', ctx, context_instance = RequestContext(request))

def vista_listar_vendedora(request):
	activo = 'active'
	foot = True
	numero = 2
	vista = 'Listar Cliente'
	vendedora = Cliente.objects.all()
	ctx ={'vendedora':vendedora, 'nombre_sistema': settings, 'foot': foot, 'vista': vista, 'numero': numero, 'activo':activo}
	return render_to_response('ver_vendedora.html', ctx, context_instance = RequestContext(request))

@login_required(login_url = '/')
def vista_editar_vendedora(request, id):
	try:
		request.META['HTTP_REFERER']
	except KeyError:
		return HttpResponseRedirect('/listar/cliente')
	foot = True
	vista = 'Editar Cliente'
	base = get_object_or_404(Cliente, pk = id )
	if request.method == 'POST':
		formulario = VendedoraForm(request.POST, request.FILES, instance=base)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/listar/cliente')
	else:
		formulario = VendedoraForm(instance = base)
	ctx ={'formulario':formulario, 'nombre_sistema': settings, 'foot': foot, 'vista': vista}
	return render_to_response('editar_vendedora.html', ctx, context_instance = RequestContext(request))

@login_required(login_url = '/')
def vista_eliminar_vendedora(request, id):
	try:
		request.META['HTTP_REFERER']
	except KeyError:
		return HttpResponseRedirect('/listar/cliente')
	foot = True
	vista = 'Eliminar Cliente'
	base = get_object_or_404(Cliente, pk = id)
	if request.method == 'POST':
		base.delete()
		return HttpResponseRedirect('/listar/cliente')
	ctx ={'foot': foot, 'vista': vista, 'nombre_sistema': settings, 'base': base}
	return render_to_response('eliminar_vendedora.html', ctx,context_instance = RequestContext(request))

@login_required(login_url = '/')
def vista_crear_encargo(request, id):
	try:
		request.META['HTTP_REFERER']
	except KeyError:
		return HttpResponseRedirect('/pizarra')

	#esta clase permite crear validaciono mejor dicho hacer cumplir la validacion de los formularios
	class Validar(BaseFormSet):
		def clean(self):

			cantidad = 0
			for form in self.forms:
				cantidad = cantidad + form.cleaned_data.get('cantidad',False)
			if cantidad == 0:
				raise 	self.forms.ValidationErro('Debe haber aun que sea un valor para realizar el pedido')
			return cantidad[0]


	vendedora_provi = get_object_or_404(Cliente, pk = id)#este campo esta asi. pero luego se haa la busqueda por medio de el id que se mandara por url
	#usuario_login = get_object_or_404(User, username = request.user.username) #Esto fue cambiado por el id del request
	usuario_login = request.user.id
	foot = True
	vista = 'Crear Encargo'
	formularioart 		= formset_factory(ParteEncagoForm, extra=4 )
	productos =""
	pedido_valido=""#sirve para mostrar el mensaje si es que el pedido es valido osea si todos sus campos no son cero
	pago_total = 0 # variable donde se guarda el total a pagar
	suma_validacion = 0# sirve para hacer la suma de los campos para ver que no sea ceros todos
	if Producto.objects.all().exists():
		productos 		= Producto.objects.filter(Q(nombre__startswith ='quesadilla') | Q(nombre__startswith = 'torta')) #sacar los id y los precios de los productos
	if request.method == 'POST':
		formulario 		= EncargoForm(request.POST)
		formset 		= formularioart(request.POST)
		contar 			= formset.initial_form_count()
		for forms in formset:#este iteracion simplemente nos sirve para saber si todos los campos cantidad son = a 0
			este = forms.save(commit=False)
			suma_validacion = suma_validacion + este.cantidad
		pedido_valido="Su pedido es igual a cero por lo tanto no a sido  valido porfabor llene los campos de forma correcta"
		if formulario.is_valid() and formset.is_valid() and not(suma_validacion == 0):
			principal 				= formulario.save(commit=False)
			principal.usuario_id 	= usuario_login
			principal.tipo 			= 3
			principal.cliente 		= vendedora_provi
			principal.grupo 		= vendedora_provi.grupo
			principal.save()
			for formu, base in zip(formset,productos):
				salvado 			= formu.save(commit=False)
				salvado.usuario_id 	= usuario_login
				salvado.tipo    	= principal
				salvado.precios 	= base.precio
				salvado.producto 	= base
				salvado.save()
				pago_total = pago_total + (base.precio*salvado.cantidad)
			#principal_pago = MasterDPPA.objects.get(pk=principal.id)
			principal.total = pago_total
			principal.save()
			return HttpResponseRedirect('/listar/cliente')
	else:
		formset         = formularioart()
		formulario 		= EncargoForm()
	ctx ={'formulario':formulario, 'nombre_sistema': settings, 'foot': foot, 'vista': vista,
								 'formset': formset, 'productos': productos,'pedido_valido': pedido_valido}
	return render_to_response('quesadilla/encargo.html', ctx, context_instance = RequestContext(request))




@login_required(login_url = '/')
def vista_pagar_encargo(request, id):
	try:
		request.META['HTTP_REFERER']
	except KeyError:
		return HttpResponseRedirect('/pizarra')

	#seccion de las queris necesarias
	#usuario_login 					= User.objects.get(username = request.user.username)
	usuario_login = request.user.id
	pedido 							= ProductoDPPA.objects.select_related('tipo').filter(tipo__id= id)
	masterdppapedido 				= MasterDPPA.objects.get(id=id)
	lista_errores = [] #aqui guardaremos los errores para tratar de hacer una validacion  por dormulario
	#seccion clase de validacion de cantidades ---------------------------------------------------------------
	class ValidacionFormset(BaseFormSet):
		def clean(self):
			super(ValidacionFormset, self).clean()
			for form, otro in zip(self.forms,pedido):
				try:
					cantidad = form.cleaned_data['cantidad']
				except(KeyError):
				   cantidad = ""
				if cantidad < 0 or cantidad > otro.cantidad or cantidad == " ":
					raise forms.ValidationError("el valor ingresado no es valido .")

	#------------------------------------------------------------------------------------------------------------------------------------------
	cuantos = None
	foot 							= True
	vista 							= 'Realizar Pago'
	formularioart 					= formset_factory(ParteEncagoForm, extra= 4, formset=ValidacionFormset)#creacion de el formset para ser utilizados en la vista
	productos 						=""
	pago_total 						= 0 # variable donde se guarda el total a pagar
	suma_validacion 				= 0
	deuda_total						= 0

	if Producto.objects.all().exists():
		productos 		= ProductoDPPA.objects.filter(tipo = masterdppapedido) #sacar los id y los precios de los productos
	if request.method == 'POST':
		deuda1 = MasterDPPA.objects.get(cliente= masterdppapedido.cliente, tipo=2)
		deuda2 	= ProductoDPPA.objects.filter(tipo=deuda1)
		formset 					= formularioart(request.POST)
		formulario 					= MasterDPPA()
		# for forms in formset:#este iteracion simplemente nos sirve para saber si todos los campos cantidad son = a 0
		# 	este = forms.cleaned_data['cantidad']
		# 	suma_validacion = suma_validacion + este
		# pedido_valido="Su pedido es igual a cero por lo tanto no a sido  valido porfabor llene los campos de forma correcta"
		if formset.is_valid():#validar si los campos no son vacios y si su contenido es correcto
			principal 				= formulario
			principal.usuario_id 	= usuario_login
			principal.tipo 			= 1
			principal.cliente 		= masterdppapedido.cliente #agregar una querry que capture el id para poderlo usar aqui jajja
			principal.basado_en     = masterdppapedido
			principal.save()
			pagarpedido 			= masterdppapedido
			pagarpedido.pago_f_v 	= True #hacer que ya estava pagado
			pagarpedido.save()

			#queri de los campos para las deudas#jalar la deuda
			deusadppa 				= MasterDPPA.objects.get(cliente=masterdppapedido.cliente, tipo=2)
			prod_deuda				= ProductoDPPA.objects.filter(tipo=deusadppa)#querry para obtener los productos donde se almacenaran las cantidades que se quedan sin pagar
			for formu, base, deuda in zip(formset, productos, prod_deuda):
				cantidades 			= formu.cleaned_data['cantidad']
				salvado 			= ProductoDPPA()
				salvado.usuario_id 	= usuario_login
				salvado.tipo    	= principal
				salvado.precios 	= base.precios
				salvado.producto 	= base.producto
				salvado.cantidad 	= cantidades
				salvado.save()
				pdeuda 				= deuda# objeto para modificar la deuda
				pdeuda.cantidad 	= pdeuda.cantidad + (base.cantidad - salvado.cantidad)
				pdeuda.save()
				pago_total = pago_total + (base.precios * salvado.cantidad)
				deuda_total = deuda_total + (base.precios*(base.cantidad - salvado.cantidad))
			#principal_pago = MasterDPPA.objects.get(pk=principal.id)
			deuda_pago = deusadppa # cosas de la deuda
			deuda_pago.total    = deuda_pago.total + deuda_total
			deuda_pago.save()
			principal.total = pago_total#terminar de el pago
			principal.save()
			# pedido_pagado = masterdppapedido#dejar el pedido como pagado para que no apares que la zona de pedido osea la pizarra
			# pedido_pagado.pago_f_v = True
			# pedido_pagado.save()#falto solucionae estas tres lineas de el pedido_pago

			return HttpResponseRedirect('/pizarra')

	else:
		formset         			= formularioart()

	ctx ={ 'nombre_sistema': settings, 'foot': foot, 'vista': vista,
								 'formset': formset, 'productos': productos, 'pedido': pedido, 'cuantos': cuantos}
	return render_to_response('quesadilla/pago.html', ctx, context_instance = RequestContext(request))

def vista_pizarra(request):
	base =  MasterDPPA.objects.values('fecha_entrega').filter(fecha_entrega = datetime.date.today(), tipo=3)
	msg = None
	if base:
		fecha = base[0]
	else:
		fecha = datetime.date.today
		msg ='Para esta fecha no se encuentra ningun pedido'
	foot = False
	sumatorias = Producto.objects.filter(Q(productodppa__tipo__entregado=True), Q(productodppa__tipo__pago_f_v=False),Q(productodppa__tipo__tipo=3),Q(productodppa__tipo__fecha_entrega=datetime.date.today()),Q(nombre__startswith ='quesadilla') | Q(nombre__startswith = 'torta')).annotate(suma =Sum('productodppa__cantidad'))
	pedido = ProductoDPPA.objects.select_related('tipo').filter(tipo__fecha_entrega=datetime.date.today(), tipo__tipo=3, tipo__pago_f_v=False, tipo__entregado=True)

	vista = 'Pizarra'
	ctx ={'fecha': fecha, 'nombre_sistema': settings, 'foot': foot, 'vista': vista, 'pedido': pedido, 'sumatorias': sumatorias, 'msg': msg, 'base': base}
	return render_to_response('quesadilla/pizarra.html', ctx, context_instance = RequestContext(request))

def vista_pizarra_entrega(request):
	base =  MasterDPPA.objects.values('fecha_entrega').filter(fecha_entrega = datetime.date.today(), tipo=3)
	msg = None
	numero = None
	errores = ""
	if base:
		fecha = base[0]
	else:
		fecha = datetime.date.today
		msg ='Para esta fecha no se encuentra ningun pedido'
	foot = False
	sumatorias = Producto.objects.filter(Q(productodppa__tipo__entregado=False),Q(productodppa__tipo__pago_f_v=False), Q(productodppa__tipo__tipo=3), Q(productodppa__tipo__fecha_entrega=datetime.date.today()),
		Q(nombre__startswith ='quesadilla') | Q(nombre__startswith = 'torta')).annotate(suma =Sum('productodppa__cantidad'))
	#query para grupos A, B, C ----------------------------------------------------------------------------------------------------------------------------------------
	pedido = ProductoDPPA.objects.select_related('tipo').filter(tipo__fecha_entrega=datetime.date.today(), tipo__tipo=3, tipo__pago_f_v=False, tipo__entregado = False)
	seccionA = ProductoDPPA.objects.select_related('tipo').filter(tipo__fecha_entrega=datetime.date.today(), tipo__tipo=3, tipo__pago_f_v=False,
	 			tipo__entregado = False, tipo__grupo = 'A')
	seccionB = ProductoDPPA.objects.select_related('tipo').filter(tipo__fecha_entrega=datetime.date.today(), tipo__tipo=3, tipo__pago_f_v=False,
	 			tipo__entregado = False, tipo__grupo = 'B')
	seccionC = ProductoDPPA.objects.select_related('tipo').filter(tipo__fecha_entrega=datetime.date.today(), tipo__tipo=3, tipo__pago_f_v=False,
	 			tipo__entregado = False, tipo__grupo = 'C')
	#------------------------------------------------------------------------------------------------------------------------------------------------------------------
	#formpedido = MasterDPPA.objects.filter(fecha_entrega=datetime.date.today(), tipo=3, pago_f_v=False, entregado = False).values()
	formulario_de_mas =	formset_factory(DemasDemenosForm, extra= 4)

	if request.method == 'POST':
		formsetpedido = formulario_de_mas(request.POST)
		if formsetpedido.is_valid():
			numero = formsetpedido.cleaned_data['id']
			de_mas = formsetpedido.cleaned_data['de_mas']
			de_menos = formsetpedido.cleaned_data['de_menos']
			entregado = MasterDPPA.objects.get(pk=numero)
			entregado.de_mas = de_mas
			entregado.de_menos = de_menos
			entregado.entregado = True
			entregado.save()
			return HttpResponseRedirect('/pizarra/entrega')
	else:
		formsetpedido =  formulario_de_mas()
	vista = 'Pizarra'
	ctx ={'fecha': fecha, 'nombre_sistema': settings, 'foot': foot, 'vista': vista, 'pedido': pedido, 'sumatorias': sumatorias, 'msg': msg, 'base': base,
	 				'formset': formsetpedido, 'numero': numero, 'seccionA': seccionA, 'seccionB': seccionB, 'seccionC': seccionC, 'errores': errores}
	return render_to_response('quesadilla/pizarra_entrega.html', ctx, context_instance = RequestContext(request))

def vista_pizarra_entrega_expres(request, id):
	entrega = MasterDPPA.object.get(id = id)
	entrega.entregado = True
	entrega.save()
	return HttpResponseRedirect('/pizarra/entrega')