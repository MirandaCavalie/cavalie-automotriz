/**
 * Libro de Reclamaciones virtual de Cavalié Automotriz (Google Forms + Apps Script).
 *
 * Qué hace:
 *  1. crearLibro(): crea el formulario con los campos de la Hoja de Reclamación
 *     (Anexo I del Reglamento del Libro de Reclamaciones, D.S. 011-2011-PCM y modificatorias),
 *     una hoja de cálculo donde se guardan las respuestas y el disparador de envío.
 *  2. alEnviar(): cada vez que alguien envía el formulario, asigna un número correlativo
 *     (N.° 000001-2026), lo anota en la hoja y envía la copia de la Hoja de Reclamación
 *     al correo del consumidor y al correo del taller.
 *
 * Cómo usarlo: ver herramientas/libro-de-reclamaciones/SOP.md
 * Antes de publicarlo, el abogado o contador del taller debe validar textos y campos.
 */

// ---------- Datos del proveedor (no cambiar sin revisar con el contador) ----------
var PROVEEDOR = {
  razonSocial: 'CARVALIE E.I.R.L.',
  ruc: '20503409021',
  nombreComercial: 'Cavalié Automotriz',
  domicilio: 'Jr. José Gálvez 1469, Santa Beatriz, Cercado de Lima, Lima',
  correo: 'cavalieautomotriz@gmail.com',
  web: 'https://cavalieautomotriz.com'
};
var PLAZO_DIAS_HABILES = 15;

// Títulos de las preguntas (se usan para leer las respuestas; no cambiarlos después de crear el formulario)
var P = {
  nombre: 'Nombre completo',
  tipoDoc: 'Tipo de documento',
  numDoc: 'Número de documento',
  domicilio: 'Domicilio',
  telefono: 'Teléfono',
  correo: 'Correo electrónico',
  menor: '¿Eres menor de edad?',
  apoderado: 'Si eres menor de edad: nombre y documento de tu padre, madre o apoderado',
  bien: 'Bien contratado',
  monto: 'Monto reclamado (S/)',
  descripcionBien: 'Descripción del servicio o producto (placa del vehículo, fecha, orden de servicio si la tienes)',
  tipo: 'Tipo',
  detalle: 'Detalle del reclamo o queja',
  pedido: 'Pedido: ¿qué solicitas?',
  conformidad: 'Declaración'
};

function crearLibro() {
  var form = FormApp.create('Libro de Reclamaciones – ' + PROVEEDOR.nombreComercial);
  form.setDescription(
    'Hoja de Reclamación virtual\n' +
    PROVEEDOR.razonSocial + ' · RUC ' + PROVEEDOR.ruc + '\n' +
    PROVEEDOR.domicilio + '\n\n' +
    'RECLAMO: disconformidad relacionada con los productos o servicios.\n' +
    'QUEJA: disconformidad no relacionada con los productos o servicios, o malestar o descontento respecto a la atención al público.\n\n' +
    'Al enviar este formulario recibirás en tu correo una copia de tu Hoja de Reclamación con su número y fecha. ' +
    'Daremos respuesta en un plazo no mayor a ' + PLAZO_DIAS_HABILES + ' días hábiles.'
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setLimitOneResponsePerUser(false);
  form.setConfirmationMessage(
    'Recibimos tu Hoja de Reclamación. En unos minutos te llegará una copia con su número a tu correo. ' +
    'Si no la ves, revisa la carpeta de spam o escríbenos a ' + PROVEEDOR.correo + '.'
  );

  form.addSectionHeaderItem().setTitle('1. Identificación del consumidor reclamante');
  form.addTextItem().setTitle(P.nombre).setRequired(true);
  form.addListItem().setTitle(P.tipoDoc).setChoiceValues(['DNI', 'Carné de extranjería', 'Pasaporte', 'RUC']).setRequired(true);
  form.addTextItem().setTitle(P.numDoc).setRequired(true);
  form.addTextItem().setTitle(P.domicilio).setRequired(true);
  form.addTextItem().setTitle(P.telefono).setRequired(true);
  form.addTextItem().setTitle(P.correo).setRequired(true)
    .setValidation(FormApp.createTextValidation().requireTextIsEmail().build());
  form.addMultipleChoiceItem().setTitle(P.menor).setChoiceValues(['No', 'Sí']).setRequired(true);
  form.addTextItem().setTitle(P.apoderado);

  form.addSectionHeaderItem().setTitle('2. Identificación del bien contratado');
  form.addMultipleChoiceItem().setTitle(P.bien).setChoiceValues(['Servicio', 'Producto']).setRequired(true);
  form.addTextItem().setTitle(P.monto)
    .setHelpText('Si no aplica, escribe 0.')
    .setValidation(FormApp.createTextValidation().requireNumber().build());
  form.addParagraphTextItem().setTitle(P.descripcionBien).setRequired(true);

  form.addSectionHeaderItem().setTitle('3. Detalle de la reclamación y pedido del consumidor');
  form.addMultipleChoiceItem().setTitle(P.tipo)
    .setChoiceValues(['Reclamo (disconformidad con el servicio o producto)', 'Queja (disconformidad con la atención)'])
    .setRequired(true);
  form.addParagraphTextItem().setTitle(P.detalle).setRequired(true);
  form.addParagraphTextItem().setTitle(P.pedido).setRequired(true);

  form.addCheckboxItem().setTitle(P.conformidad)
    .setChoiceValues(['Declaro que los datos consignados son verdaderos y acepto la Política de privacidad (' + PROVEEDOR.web + '/politica-de-privacidad/).'])
    .setRequired(true);

  // Hoja de cálculo para las respuestas
  var hoja = SpreadsheetApp.create('Libro de Reclamaciones – respuestas');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, hoja.getId());

  // Disparador: al enviar
  ScriptApp.newTrigger('alEnviar').forForm(form).onFormSubmit().create();

  PropertiesService.getScriptProperties().setProperties({
    hojaId: hoja.getId(),
    correlativo: '0'
  });

  Logger.log('Formulario para el público: ' + form.getPublishedUrl());
  Logger.log('Editar formulario: ' + form.getEditUrl());
  Logger.log('Hoja de respuestas: ' + hoja.getUrl());
}

function alEnviar(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var props = PropertiesService.getScriptProperties();
    var n = Number(props.getProperty('correlativo') || '0') + 1;
    props.setProperty('correlativo', String(n));
    var anio = Utilities.formatDate(new Date(), 'America/Lima', 'yyyy');
    var numero = 'N.° ' + ('000000' + n).slice(-6) + '-' + anio;
    var fecha = Utilities.formatDate(e.response.getTimestamp(), 'America/Lima', 'dd/MM/yyyy HH:mm');

    var r = {};
    e.response.getItemResponses().forEach(function (ir) {
      var v = ir.getResponse();
      r[ir.getItem().getTitle()] = Array.isArray(v) ? v.join(', ') : v;
    });

    anotarEnHoja_(props.getProperty('hojaId'), e.response.getTimestamp(), numero);

    var html = hojaHtml_(numero, fecha, r);
    var asunto = 'Hoja de Reclamación ' + numero + ' – ' + PROVEEDOR.nombreComercial;
    MailApp.sendEmail({
      to: r[P.correo],
      cc: PROVEEDOR.correo,
      replyTo: PROVEEDOR.correo,
      name: PROVEEDOR.nombreComercial,
      subject: asunto,
      htmlBody: html
    });
  } finally {
    lock.releaseLock();
  }
}

// Agrega el número correlativo en la fila de la respuesta (columna "N.° de hoja")
function anotarEnHoja_(hojaId, marca, numero) {
  if (!hojaId) return;
  var sh = SpreadsheetApp.openById(hojaId).getSheets()[0];
  var cab = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  var col = cab.indexOf('N.° de hoja') + 1;
  if (col === 0) {
    col = sh.getLastColumn() + 1;
    sh.getRange(1, col).setValue('N.° de hoja');
    sh.getRange(1, col + 1).setValue('Respuesta del proveedor');
    sh.getRange(1, col + 2).setValue('Fecha de respuesta');
  }
  var marcas = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 1).getValues();
  for (var i = marcas.length - 1; i >= 0; i--) {
    if (marcas[i][0] instanceof Date && Math.abs(marcas[i][0] - marca) < 5000) {
      sh.getRange(i + 2, col).setValue(numero);
      return;
    }
  }
}

function hojaHtml_(numero, fecha, r) {
  function fila(k, v) {
    return '<tr><td style="padding:6px 10px;border:1px solid #DCE1EC;background:#F4F6FB;width:38%"><b>' + k +
      '</b></td><td style="padding:6px 10px;border:1px solid #DCE1EC">' + (v ? String(v).replace(/</g, '&lt;') : '—') + '</td></tr>';
  }
  return '<div style="font-family:Arial,sans-serif;color:#0B1233;max-width:640px">' +
    '<h2 style="margin:0 0 4px">Hoja de Reclamación ' + numero + '</h2>' +
    '<p style="margin:0 0 16px;color:#3B4466">Fecha: ' + fecha + '</p>' +
    '<table style="border-collapse:collapse;width:100%;font-size:14px">' +
    fila('Proveedor', PROVEEDOR.razonSocial + ' (' + PROVEEDOR.nombreComercial + ')') +
    fila('RUC', PROVEEDOR.ruc) + fila('Domicilio del proveedor', PROVEEDOR.domicilio) +
    fila('Consumidor', r[P.nombre]) + fila('Documento', r[P.tipoDoc] + ' ' + r[P.numDoc]) +
    fila('Domicilio', r[P.domicilio]) + fila('Teléfono', r[P.telefono]) + fila('Correo', r[P.correo]) +
    fila('Menor de edad', r[P.menor]) + fila('Padre, madre o apoderado', r[P.apoderado]) +
    fila('Bien contratado', r[P.bien]) + fila('Monto reclamado (S/)', r[P.monto]) +
    fila('Descripción', r[P.descripcionBien]) + fila('Tipo', r[P.tipo]) +
    fila('Detalle', r[P.detalle]) + fila('Pedido', r[P.pedido]) +
    fila('Observaciones y acciones del proveedor', 'Pendiente de respuesta') +
    '</table>' +
    '<p style="font-size:13px;color:#3B4466;margin-top:16px">' +
    'El proveedor deberá dar respuesta al reclamo o queja en un plazo no mayor a ' + PLAZO_DIAS_HABILES + ' días hábiles. ' +
    'La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.</p>' +
    '<p style="font-size:13px;color:#3B4466">Para cualquier consulta sobre esta hoja, responde a este correo o escribe a ' + PROVEEDOR.correo + '.</p>' +
    '</div>';
}
