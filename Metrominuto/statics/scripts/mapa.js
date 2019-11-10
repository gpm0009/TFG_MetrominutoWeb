 // JavaScript source code
 function inicializar() {
  //Opciones del mapa
  var OpcionesMapa = {
      center: new google.maps.LatLng(38.3489719, -0.4780289000000266),
      mapTypeId: google.maps.MapTypeId.ROADMAP, //ROADMAP  SATELLITE HYBRID TERRAIN
      zoom: 16
  };

  var map;
  //constructor
  map = new google.maps.Map(document.getElementById('map'), OpcionesMapa);

  //Añadimos el marcador
  var Marcador = new google.maps.Marker({
                  position: new google.maps.LatLng(38.3489719, -0.4780289000000266),
                  map: map
              });
}

function CargaScript() {
  var script = document.createElement('script');
  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBa4H59vDquLKttwMkxv0WaJrx3wXB260s&callback=initMap';
  document.body.appendChild(script);                 
}

window.onload = CargaScript;