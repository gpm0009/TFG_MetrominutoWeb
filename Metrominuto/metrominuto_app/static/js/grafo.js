function draw_graphs(svg_list) {
    for(var i=0;i<svg_list.length;i++){
        console.log(i);
    }
    var svg = document.getElementById("mysvg");
    svg.innerHTML = svg_list[0];
    $("#formControlRange").change(function () {
        console.log($('#formControlRange').val());
        var svg = document.getElementById("mysvg");
        svg.innerHTML = svg_list[$('#formControlRange').val()];
    });
}