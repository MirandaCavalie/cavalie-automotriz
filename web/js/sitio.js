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

  // Carruseles continuos (reseñas y logos): duplica el contenido para un recorrido sin cortes
  document.querySelectorAll('.carrusel').forEach(function (carrusel) {
    var pista = carrusel.querySelector('.carrusel__pista');
    Array.prototype.slice.call(pista.children).forEach(function (r) {
      var copia = r.cloneNode(true); copia.setAttribute('aria-hidden', 'true'); copia.setAttribute('alt', ''); pista.appendChild(copia);
    });
  });

  // Trabajos realizados: flechas que deslizan la fila una foto a la vez
  var fila = document.getElementById('trabajos-fila');
  if (fila) {
    document.querySelectorAll('.flecha').forEach(function (b) {
      b.addEventListener('click', function () {
        var paso = fila.querySelector('.trabajo').offsetWidth + 20;
        fila.scrollBy({ left: paso * Number(b.getAttribute('data-dir')), behavior: 'smooth' });
      });
    });
  }

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
