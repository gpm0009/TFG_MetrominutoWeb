function muestra_oculta_mapa(){
    var mapa = document.getElementById('ayuda_mapa');
    mapa.style.display = 'block';
    var grafo = document.getElementById('ayuda_grafo');
    grafo.style.display = 'none';
    var active = document.getElementById('map-button');

}

function muestra_oculta_grafo(){
    var mapa = document.getElementById('ayuda_mapa');
    mapa.style.display = 'none';
    var grafo = document.getElementById('ayuda_grafo');
    grafo.style.display = 'block' ;
}

$(function(){
  $('body').on('click', '.list-group-item', function(){
    $('.list-group-item').removeClass('active');
    $(this).closest('.list-group-item').addClass('active');
  });
});