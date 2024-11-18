const listarcliente = async (idcliente) => {
    try {
        const response = await fetch(`../cliente/${idcliente}`);
        
        
        const data = await response.json();
        console.log(data);
        if (data.messages == "Satisfactorio") {
            CargarCliente.innerHTML = data.clientes;
        } else {
            alert("cliente no encontrados");
        }
    
    
    
    } catch (error) {
        console.log(error);
    }

};






const listarusuarios = async () => {
    try {
        const response = await fetch("../usuarios");
        const data = await response.json();
        console.log(data);
        if (data.messages == "Satisfactorio") {
            let opciones = ``;
            data.usuarios.forEach((usu) => {
                opciones+=`<option value='${usu.usuario_id}'>${usu.nombreusuario}</option>`;
            });
            Clien.innerHTML = opciones;
        } else {
            alert("usuarios no encontrados");
        }
    
    
    
    } catch (error) {
        console.log(error);
    }

};


const cargaInicial = async () => {
    await listarusuarios();

    Clien.addEventListener("change", (event) => {
        listarcliente(event.target.value);
    });

};


window.addEventListener("load", async () => {
    await cargaInicial();
});
