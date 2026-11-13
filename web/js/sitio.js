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

  // Trabajos realizados: carrusel que avanza solo y se puede arrastrar con el mouse
  var fila = document.getElementById('trabajos-fila');
  if (fila) {
    var originales = Array.prototype.slice.call(fila.children);
    originales.forEach(function (f) { var c = f.cloneNode(true); c.setAttribute('aria-hidden', 'true'); fila.appendChild(c); });
    var vuelta = function () { return fila.children[originales.length].offsetLeft - originales[0].offsetLeft; };
    var pos = 0, pausa = false, arrastre = null, reanudar;
    var quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var ajustar = function () { var v = vuelta(); if (pos >= v) pos -= v; if (pos < 0) pos += v; fila.scrollLeft = pos; };
    var esperar = function (ms) { pausa = true; clearTimeout(reanudar); reanudar = setTimeout(function () { pos = fila.scrollLeft; pausa = false; }, ms); };
    (function paso() {
      if (!pausa && !arrastre && !quieto) { pos += 0.5; ajustar(); }
      requestAnimationFrame(paso);
    })();
    fila.addEventListener('mouseenter', function () { pausa = true; clearTimeout(reanudar); });
    fila.addEventListener('mouseleave', function () { if (!arrastre) esperar(600); });
    fila.addEventListener('touchstart', function () { pausa = true; clearTimeout(reanudar); }, { passive: true });
    fila.addEventListener('touchend', function () { esperar(2500); });
    fila.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse') return;
      arrastre = { x: e.clientX, inicio: fila.scrollLeft };
      fila.classList.add('arrastrando'); fila.setPointerCapture(e.pointerId);
    });
    fila.addEventListener('pointermove', function (e) {
      if (!arrastre) return;
      pos = arrastre.inicio - (e.clientX - arrastre.x); ajustar();
    });
    var soltar = function () { if (!arrastre) return; arrastre = null; fila.classList.remove('arrastrando'); pos = fila.scrollLeft; };
    fila.addEventListener('pointerup', soltar);
    fila.addEventListener('pointercancel', soltar);
    fila.addEventListener('dragstart', function (e) { e.preventDefault(); });
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
