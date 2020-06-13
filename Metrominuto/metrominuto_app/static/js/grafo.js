function draw_graphs(svg_list, colors) {
    var svg = document.getElementById("mysvg");
    svg.innerHTML = svg_list[0];
    $("#formControlRange").change(function () {
        var control_val = $('#formControlRange').val()
        var svg = document.getElementById("mysvg");
        svg.innerHTML = svg_list[$('#formControlRange').val()];
        document.getElementById("color_green").innerHTML=colors[control_val]['green'];
        document.getElementById("color_blue").innerHTML=colors[control_val]['blue'];
        document.getElementById("color_brown").innerHTML=colors[control_val]['brown'];
        document.getElementById("color_purple").innerHTML=colors[control_val]['purple'];
        document.getElementById("color_red").innerHTML=colors[control_val]['red'];
    });
}