// Ahora (Castilla y León)
const map = L.map('map').setView([41.7, -4.5], 8);
// Capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let startMarker, endMarker;
let routeLayers = [];

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
    console.log('data', data.length, data)

    // Eliminar rutas anteriores
    routeLayers.forEach(layer => map.removeLayer(layer));
    routeLayers = [];

    // Colores para distinguir rutas
    const colors = ["blue", "red", "green"];

    let allCoords = [];  // Para calcular bounds de todas las rutas

    data.forEach((route, index) => {
        const coords = route.geometry.coordinates.map(c => [c[1], c[0]]);
        allCoords = allCoords.concat(coords);

        const polyline = L.polyline(coords, {
            color: colors[index % colors.length],
            weight: 5,
            opacity: 0.8
        }).addTo(map);

        // Puedes guardar info adicional en el polyline
        polyline.routeId = route.id;
        polyline.safetyIndex = route.safety_index;

        routeLayers.push(polyline);
    });

    if (allCoords.length > 0) {
        map.fitBounds(allCoords);
    }
}
console.log("script cargado");
document.getElementById("routeBtn").addEventListener("click", getRoute);
