function muestra_oculta_mapa(){
    var mapa = document.getElementById('ayuda_mapa');
    mapa.style.display = 'block';
    var grafo = document.getElementById('ayuda_grafo');
    grafo.style.display = 'none';
}

function muestra_oculta_grafo(){
    var mapa = document.getElementById('ayuda_mapa');
    mapa.style.display = 'none';
    var grafo = document.getElementById('ayuda_grafo');
    grafo.style.display = 'block' ;
}