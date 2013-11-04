$(document).ready(function() {
	//--------------------------------------------------
	//prueva
	//----------------------------------------------------

	//--------------------------------------------------
	//toggle de la pizarra de entregas
	//----------------------------------------------------
	$( '.accion').click(function() {
		var padre = $(this).attr('name');
		$( "clase22" ).css('display','none');
  		$(padre).slideToggle( "slow" );
	});
	//--------------------------------------------------
	//para hacer las alertas de bootstrap
	//----------------------------------------------------

	//--------------------------------------------------
	//cambio de atributos de algunos campos y aplicacion de la mascara de rellenado para otros
	//----------------------------------------------------
	$('#id_fnacimiento , #id_fecha_ingreso, #id_fecha, #id_fecha_entrega, #id_fecha_naciemiento, #id_fecha_contratacion').addClass('calendario');
	$('#id_activo').addClass('switch-left');
	$("#id_dui").mask("99999999-9",{placeholder:" "});
	$("#id_telefono, #id_contacto_e_t").mask("9999-9999",{placeholder:" "});
	$('#id_pmail, #id_mmail, #id_email').attr('type', 'email');
	//--------------------------------------------------
	//controla las opciones de el datepicker
	//--------------------------------------------------
	$(function(){
			$( ".calendario " ).datepicker({
				changeMonth: true,
				changeYear: true,
				dateFormat: "dd/mm/yy",
				monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
				minDate:  Number(0),
				dayNamesMin: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'],
				nextText:'Siguiente',
				prevText:'Previo',
			});
		});

	//--------------------------------------------------
	//codigo que controla el tipo de tooltip o poopup
	//---------------------------------------------------
	$(function() {
	    $( document ).tooltip({
	      position: {
	        my: " bottom-10",
	        at: "top",
	        using: function( position, feedback ) {
	          $( this ).css( position );
	          $( "<div>" )
	            .addClass( "arrow" )
	            .addClass( feedback.vertical )
	            .addClass( feedback.horizontal )
	            .appendTo( this );
	         }
	       }
	    });
	 });
	//--------------------------------------------------
	// $(function(){
	// 	$('#id_nombres').attr('title','Hola mundo');
	// });
	//---------------------------------------------------
	//concatenacion de campos para  campo codigo del alumno
	//----------------------------------------------------
	var espacio = 0
	$('input').keyup(function(){
		//capturar los dos ultimos numeros de el año
		var fecha = $('#id_fnacimiento').val().substring(8,10);
		var letras = "";
		//crear una sola lista con los  nombre  y los apellidos
		concatenar = ($('#id_apellidos').val().split(" "));
		//sacar las iniciales
		$.each(concatenar,function(k,v){
			letras = letras + v.substr(0,1);
		});
		//ingresar el texto unido para el codigo;
		$("#id_codigo_alumno").val( letras + fecha + '-' );
	});
});

