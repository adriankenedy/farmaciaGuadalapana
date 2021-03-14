var operacion = '';
function mostrarDiv(div, bandera) {
    if (bandera == true) {
        document.getElementById(div).style.display = 'block';
    } else {
        document.getElementById(div).style.display = 'none';
    }
}

function inicializarDivs() {
    operacion = '';
    mostrarDiv('listadoGeneral', true);
    mostrarDiv('listadoIndividual', false);
    consultaGeneral();

}
function carrito() {
    operacion = 'i';
    consultarId();
    mostrarDiv("listadoIndividual", true);
    mostrarDiv("listadoGeneral", false);
    limpirControles();
}

function editar(id) {
    operacion = "u";
    consultaIndividual(id);
    mostrarDiv("listadoIndividual", true);
    mostrarDiv("listadoGeneral", false);
}

function consultaGeneral() {
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function () {
        if (this.status == 200 && this.readyState == 4) {
            llenarTabla(this.responseText);
        }
    };
    ajax.open("get", "/consultarOpciones", true);
    ajax.send();
}


function llenarTabla(respuesta) {
    var datos = JSON.parse(respuesta);
    limpiarTabla();
    var table = document.getElementById("datos");
    for (i = 0; i < datos.length; i++) {
        var tr = document.createElement("tr");
        var opcion = datos[i];
        for (propiedad in opcion) {
            var td = document.createElement("td");
            var text = document.createTextNode(opcion[propiedad]);
            td.appendChild(text);
            tr.appendChild(td);
        }
        table.appendChild(tr);
        var td = document.createElement("td");
        td.appendChild(crearLink(opcion.id, "editar"));
        tr.appendChild(td);
        table.appendChild(tr);
        td = document.createElement("td");
        td.appendChild(crearLink(opcion.id, "eliminar"));
        tr.appendChild(td);
        table.appendChild(tr);
    }
}


function consultarId(){
    var url="/ultimoIdOpcion";
    var ajax=new XMLHttpRequest();
    ajax.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            document.getElementById("id").value=this.responseText;
        }
    };
    ajax.open("get",url,true);
    ajax.send();
}