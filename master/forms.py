#encoding:utf-8
from django.forms import ModelForm,PasswordInput
from django import forms
from master.models import *
import datetime
from django.forms.widgets import PasswordInput
class VendedoraForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ('usuario',)

class EncargoForm(forms.ModelForm):
    class Meta:
        model = MasterDPPA
        exclude = ('cliente', 'tipo', 'usuario', 'pago_f_v', 'grupo')
    def clean_fecha_entrega(self):
    	fecha_entrega = self.cleaned_data.get('fecha_entrega',False)
    	fecha_hoy = datetime.date.today()- datetime.timedelta(-1)
    	if fecha_entrega < fecha_hoy:
    		msg = 'la Fecha no puede ser ni igual  ni menor a el dia de hoy %s. minmo debe de eser esta fecha %s' % (datetime.date.today(),fecha_hoy)
    		raise forms.ValidationError(msg)
    	return fecha_entrega

class ParteEncagoForm(forms.Form):
	cantidad      = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'value': 0}))

class LoginForm(forms.Form):
    usuario         = forms.CharField(max_length=20)
    contrasena      = forms.CharField(max_length=20 ,widget = PasswordInput(), label='Contraseña')

class DemasDemenosForm(forms.Form):
    ''' formulario para manejar las cantidades que se daran de mas o de menos
        como compenzaciones a los clientes por alguna razon no definida explicitamente  '''
    def clean(self):
        cleaned_data = super(DemasDemenosForm, self).clean()
        de_mas      =   cleaned_data.get("de_mas")
        de_menos    =   cleaned_data.get("de_menos")
        msg = 'los valores ingresados no son validos solo se puede ingresar uno u otro '
        msg1 = 'los valores ingresados no son validos ya que son menores acero'

        if int(de_mas) != 0 and int(de_menos) != 0:
            errores = 'Tosdos campos no pueden contener datos al mismo tiempo'
            raise forms.ValidationError(msg)
        else:
            if int(de_mas) < 0:
                errores = "el dato de menos no puede ser menos a cero "
                raise forms.ValidationError(msg1)

            if int(de_menos) < 0:
                errores = "el dato de menos no puede ser menos a cero "
                raise forms.ValidationError(msg1)

        return cleaned_data

    id            = forms.IntegerField()
    de_mas        = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={ 'value': 0, 'size':12}))
    de_menos      = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={ 'value': 0, 'size':2}))

class Busqueda(forms.Form):
    criterio         = forms.CharField(label ='nombre', max_length=50)
