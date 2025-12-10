// Crear mapa centrado en Madrid
const map = L.map('map').setView([40.4168, -3.7038], 14);

// Capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let startMarker, endMarker;
let routeLayer;

// Elegir puntos al hacer clic
map.on('click', function(e) {
    if (!startMarker) {
        startMarker = L.marker(e.latlng, {draggable: true}).addTo(map).bindPopup("Inicio").openPopup();
    } else if (!endMarker) {
        endMarker = L.marker(e.latlng, {draggable: true}).addTo(map).bindPopup("Fin").openPopup();
    }
});

// Función para pedir ruta al backend
async function getRoute() {
    if (!startMarker || !endMarker) {
        alert("Selecciona inicio y fin en el mapa");
        return;
    }

    const start = `${startMarker.getLatLng().lat},${startMarker.getLatLng().lng}`;
    const end = `${endMarker.getLatLng().lat},${endMarker.getLatLng().lng}`;

    const res = await fetch(`/api/v1/routes/?start=${start}&end=${end}`);
    const data = await res.json();

    if (routeLayer) map.removeLayer(routeLayer);

    // Dibujar la primera ruta devuelta por el backend
    if (data.length > 0) {
        const coords = data[0].geometry.coordinates.map(c => [c[1], c[0]]);
        routeLayer = L.polyline(coords, {color: 'blue'}).addTo(map);
        map.fitBounds(routeLayer.getBounds());
    }
}

document.getElementById("routeBtn").addEventListener("click", getRoute);
