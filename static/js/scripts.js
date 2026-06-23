async function automatizarTodasLasImagenes() {
    if (!confirm("¿Deseas buscar imágenes reales para los productos?")) return;

    const productos = document.querySelectorAll('.col'); 
    
    for (const p of productos) {
        const nombreElemento = p.querySelector('.nombre-producto-title');
        const contenedorImg = p.querySelector('.contenedor-foto-interactivo');
        if (!nombreElemento || !contenedorImg) continue;
        
        const nombre = nombreElemento.innerText.trim();
        const id = p.id.replace('tarjeta-producto-', '');
        
        // Usamos LoremFlickr, es excelente para buscar comida por nombre
        const urlBusqueda = `https://loremflickr.com/600/400/${encodeURIComponent(nombre)}`;

        // 1. Actualización visual instantánea (sin recargar la página)
        let img = contenedorImg.querySelector('.img-platillo');
        if (!img) {
            img = document.createElement('img');
            img.className = 'w-100 h-100 object-fit-cover img-platillo';
            contenedorImg.appendChild(img);
        }
        img.src = urlBusqueda;
        
        // 2. Guardado en base de datos (background)
        const formData = new FormData();
        formData.append('nueva_imagen', urlBusqueda);
        formData.append('csrfmiddlewaretoken', CSRF_TOKEN);

        try {
            await fetch(URL_CAMBIAR_IMAGEN.replace('0', id), {
                method: 'POST',
                body: formData
            });
            console.log(`Imagen de ${nombre} actualizada.`);
        } catch (e) { 
            console.error("Error al guardar en BD:", e); 
        }
    }
    alert("¡Proceso finalizado! Las imágenes se han actualizado.");
}