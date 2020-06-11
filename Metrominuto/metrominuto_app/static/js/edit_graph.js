var lista = []
var lista_labels = []
//draw_graph(grap);

var papers = Snap("#svgout");
papers.attr({viewBox:"0, 0.2, 1, 1.5"});



$( "#dropdown" ).click(function() {
    $( "#leyenda" ).slideToggle( "slow");
});

Snap.plugin(function (Snap, Element, Paper, global, Fragment) {
    function dragStart(x, y, e) {
        this.current_transform = this.transform();
    }

    function dragMove(dx, dy, x, y, e) {
        this.transform(this.current_transform+'T'+dx/1000+','+dy/1000);
        this.updatePaths();
    }

    function dragEndCircle(e) {
        this.current_transform = this.transform();
        grap['nodes'][lista.indexOf(this)]['pos'] = [this.matrix.e, this.matrix.f];
        $.ajax({
            type : 'POST',
            url : "{{url_for('main.recalcule')}}",
            contentType: 'application/json;charset=UTF-8',
            data : JSON.stringify(grap)
        }).done(function(response) {
            papers.clear();
            lista = []
            lista_labels = []
            draw_graph(response);
        }).fail(function() {
            console.log('FAIL');
        });
    }

    function dragEnd(e) {
        this.current_transform = this.transform();
        grap['labels'][lista_labels.indexOf(this)]['changed'] = 1;
        grap['labels'][lista_labels.indexOf(this)]['pos'] = [this.matrix.e, this.matrix.f];
    }

    function updatePaths() {
        var key;
        for(key in this.paths) {
            this.paths[key][0].attr({"path" : this.getPathString(this.paths[key][1])});
            this.paths[key][0].prependTo(this.paper);
        }
    }

    function getCoordinates() {
        return [this.matrix.e + (this.node.width.baseVal.value / 2),
            this.matrix.f + (this.node.height.baseVal.value / 2)];
    }

    function getPathString(obj) {
        var p1 = this.getCoordinates();
        var p2 = obj.getCoordinates();
        return "M"+p1[0]+","+p1[1]+"L"+p2[0]+","+p2[1];
    }

    function addPath(obj, color) {
        var id = obj.id;
        var path = this.paper.path(this.getPathString(obj)).attr({fill:'none', stroke:color, strokeWidth:0.009});
        path.prependTo(this.paper);
        this.paths[id] = [path, obj];
        obj.paths[this.id] = [path, this];
    }

    function removePath(obj) {
        var id = obj.id;
        if (this.paths[id] != null) {
            this.paths[id][0].remove();
            this.paths[id][1] = null;
            delete this.paths[id];

            obj.paths[this.id][1] = null;
            delete obj.paths[this.id];
        }
    }

    Paper.prototype.draggableRect = function (x, y, w, h) {
        var rect = this.rect(0,0,w,h).transform("T"+x+","+y);
        rect.paths = {};
        rect.drag(dragMove, dragStart, dragEnd);
        rect.updatePaths = updatePaths;
        rect.getCoordinates = getCoordinates;
        rect.getPathString = getPathString;
        rect.addPath = addPath;
        rect.removePath = removePath;
        return rect;
    };

    function getCoordinatesCircle() {
        return [this.matrix.e, this.matrix.f];
    }

    Paper.prototype.draggableCircle = function (x, y, r, id_circle) {
        var circle = this.circle(0, 0, r).attr({id: id_circle}).transform("T"+x+","+y);
        circle.paths = {};
        circle.drag(dragMove, dragStart, dragEndCircle);
        circle.updatePaths = updatePaths;
        circle.getCoordinates = getCoordinatesCircle;
        circle.getPathString = getPathString;
        circle.addPath = addPath;
        circle.removePath = removePath;
        //circle.addClass('circle');
        return circle;
    };

    Paper.prototype.draggableText = function (cx, cy, label,w,h, id_label, label_color) {
        var text = this.text(0, 0, label).attr({id: id_label, 'font-size':0.025, 'font-weight': 'bold', fill:label_color}).transform("T"+cx+","+cy);
        text.paths = {};
        text.drag(dragMove, dragStart, dragEnd);
        text.updatePaths = updatePaths;
        text.getCoordinates = getCoordinatesCircle;
        text.getPathString = getPathString;
        text.addPath = addPath;
        text.removePath = removePath;
        return text;
    };

});

function draw_graph(grafo) {
    for(var i=0;i<grafo['nodes'].length;i++){
        //lista.push(papers.draggableRect(grafo['nodes'][i][1]['pos'][0],grafo['nodes'][i][1]['pos'][1],0.05,0.05));
        lista.push(papers.draggableCircle(grafo['nodes'][i]['pos'][0],grafo['nodes'][i]['pos'][1],0.02, 'node_'+i.toString()));
    }

    for(var i=0;i<grafo['edges'].length;i++) {
        lista[parseInt(grafo['edges'][i]['edge'][0])].addPath(lista[parseInt(grafo['edges'][i]['edge'][1])], grafo['edges'][i]['color'])
    }

    for(var i=0;i<grafo['labels'].length;i++) {
        cx =grafo['labels'][i]['pos'][0];
        cy =grafo['labels'][i]['pos'][1];
        clabel = grafo['labels'][i]['label']
        //papers.text(cx, cy, clabel).attr({'font-size':0.025, 'font-weight': 'bold'});
        if(grafo['labels'][i]['node'] == 'None'){
            var text = papers.draggableText(cx, cy, clabel,0.13,0.08, 'label_edge_'+grafo['labels'][i]['edge'][0]+grafo['labels'][i]['edge'][1], grafo['labels'][i]['color']);
            lista_labels.push(text);
        }else {
            var text = papers.draggableText(cx, cy, clabel,0.13,0.08, 'label_node'+grafo['labels'][i]['node'], grafo['labels'][i]['color']);
            lista_labels.push(text);
        }
    }
}


$("[id^=label_node]").click(function (event) {
    bootbox.prompt({
        title: "Introduzca el nuevo nombre:",
        centerVertical: true,
        value: $('#' + event.target.id).text(),
        callback: function(result){
            if (result != null) {
                Snap('#' + event.target.id).attr({'text': result});
            }
        }
    });
});

function triggerDownload (imgURI, fileName) {
    var evt = new MouseEvent("click", {
        view: window,
        bubbles: false,
        cancelable: true
    });
    var a = document.createElement("a");
    a.setAttribute("download", fileName);
    a.setAttribute("href", imgURI);
    a.setAttribute("target", '_blank');
    a.dispatchEvent(evt);
}

$("#export").on("click", function() {
    var canvas = document.createElement("canvas");
    var ctx = canvas.getContext('2d');
    var svg = document.getElementById('svgout');
    var svg_widht = svg.getBBox().widht;
    var svg_height = svg.getBBox().height;
    ctx.clearRect(0, 0, svg_widht, svg_height);

    var DOMURL = window.URL || window.webkitURL || window;
    var img1 = new Image();
    var url = papers.toDataURL();
    img1.onload = function() {
        ctx.drawImage(img1, 0, 0);
        //var png = canvas.toDataURL("image/png");
        //var mg = document.createElement("img");
        //mg.setAttribute("src", png);
        //document.body.appendChild(mg);
        DOMURL.revokeObjectURL(url);
        var imgURI = canvas
            .toDataURL("image/png")
            .replace("image/png", "image/octet-stream");
        triggerDownload(imgURI, 'fileName.png');

    }
    img1.src = url;
    /*svg_xml = (new XMLSerializer()).serializeToString(document.getElementById('svgout'));
    var canvas = document.createElement("canvas");
    var ctx = canvas.getContext('2d');

    // this is just a JavaScript (HTML) image
    var img = new Image();
    // http://en.wikipedia.org/wiki/SVG#Native_support
    // https://developer.mozilla.org/en/DOM/window.btoa
    img.src = papers.toDataURL();

    img.onload = function() {
        // after this, Canvas’ origin-clean is DIRTY
        ctx.drawImage(img, 0, 0);
    };*/
    console.log(canvas.toDataURL("image/png"));
});
/*$("#export").on("click", function() {
    var canv = document.getElementById('mycanvas');
    var ctx = canv.getContext('2d');
    ctx.arc(6, 6, 2, 0, 2 * Math.PI);
    ctx.stroke();
});*/