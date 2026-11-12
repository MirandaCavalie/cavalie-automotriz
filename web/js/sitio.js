// Cavalié Automotriz — menú móvil, formulario a WhatsApp y medición de clics.
(function () {
  var WHATSAPP = '51983745377';
  window.dataLayer = window.dataLayer || [];

  // Menú en móvil
  var boton = document.querySelector('.menu-boton');
  var menu = document.getElementById('menu');
  if (boton && menu) {
    boton.addEventListener('click', function () {
      var abierto = menu.classList.toggle('abierto');
      boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    });
  }

  // Cada clic a WhatsApp se envía a GTM como evento "whatsapp_click" (conversión de Ads/GA4)
  document.addEventListener('click', function (e) {
    var enlace = e.target.closest('a[href*="wa.me/"]');
    if (enlace) {
      window.dataLayer.push({ event: 'whatsapp_click', ubicacion: enlace.getAttribute('data-ubicacion') || 'enlace' });
    }
  });

  // Formulario de cotización: arma el mensaje y abre WhatsApp (no se guarda nada en el servidor)
  var form = document.getElementById('form-cotizar');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; };
      var mensaje = 'Hola, soy ' + v('nombre') + '. Mi vehículo es ' + v('vehiculo') +
        ', placa ' + v('placa') + '. Quiero cotizar: ' + v('servicio') + '.';
      if (v('mensaje')) { mensaje += '\n' + v('mensaje'); }
      window.dataLayer.push({ event: 'whatsapp_click', ubicacion: 'formulario', servicio: v('servicio') });
      window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(mensaje), '_blank', 'noopener');
    });
  }
})();
