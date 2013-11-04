from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('master.views',
	url(r'^$', 'vista_index', name = 'inicio'),
	url(r'^crear/cliente/$', 'vista_crear_vendedora', name = 'cliente_crear'),
	url(r'^listar/cliente/$', 'vista_listar_vendedora', name = 'cliente_listar'),
	url(r'^editar/cliente/(?P<id>\d+)/$', 'vista_editar_vendedora', name = 'cliente_editar'),
	url(r'^eliminar/cliente/(?P<id>\d+)/$', 'vista_eliminar_vendedora', name = 'cliente_eliminar'),
	url(r'^crear/pedido/(?P<id>\d+)/$', 'vista_crear_encargo', name = 'pedido_crear'),
	url(r'^pizarra/$', 'vista_pizarra', name = 'pizarra'),
	url(r'^pagar/pedido/(?P<id>\d+)/$', 'vista_pagar_encargo', name = 'pedido_pagar'),
	url(r'^logout/$','logout_vista', name='logout'),
	url(r'^pizarra/entrega/$', 'vista_pizarra_entrega', name = 'pizarra_entrega'),
	url(r'^pizarra/entrega/expres/(?P<id>\d+)/$', 'vista_pizarra_entrega_expres', name = 'pizarra_entrega_expres'),
	url(r'^pizarra/entrega/grupo(?P<grupo>\w+)$', 'vista_pizarra_grupos_cambios', name = 'pizarra_grupos_cambios'),


)