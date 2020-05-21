function draw_graphs(svg_list) {
    var svg = document.getElementById("mysvg");
    svg.innerHTML = svg_list[0];
    $("#formControlRange").change(function () {
        console.log($('#formControlRange').val());
        var svg = document.getElementById("mysvg");
        svg.innerHTML = svg_list[$('#formControlRange').val()];
    });
}