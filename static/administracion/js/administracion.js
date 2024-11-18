const listarusuarios = async () => {
    try {
        const response = await fetch("{% url 'usuarios' %}");
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.log(error);
    }

};


const cargaInicial = async () => {
    await listarusuarios();
};


window.addEventListener("load", async () => {
    await cargaInicial();
});
