// Declaración de variables globales para el mapa, el servicio de direcciones,
// la visualización de direcciones, y el estado de la jornada.
var map;
var directionsService;
var directionsDisplay;
var journeyInProgress = false;
var journeyMarker;
var stepIndex = 0;
var originPoint;
var destinationPoint;

// Función de inicialización del mapa, llamada al cargar la API de Google Maps.
function initMap() {
    // Crear un nuevo mapa centrado en una ubicación específica con cierto zoom.
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 4.710989, lng: -74.072092 },
        zoom: 12,
        // Estilos personalizados para el mapa, en este caso, desactivar las etiquetas de los puntos de interés.
        styles: [
            {
                "featureType": "poi",
                "elementType": "labels",
                "stylers": [
                    { "visibility": "off" }
                ]
            }
        ]
    });

    // Inicializar el servicio de direcciones y la visualización de direcciones en el mapa.
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true,
        polylineOptions: {
            strokeColor: "#007bff", // Color de la ruta
            strokeWeight: 5 // Grosor de la línea de la ruta
        }
    });

    // Configurar la autocompletación de los campos de origen y destino.
    var originInput = document.getElementById('origin');
    var destinationInput = document.getElementById('destination');
    var originAutocomplete = new google.maps.places.Autocomplete(originInput);
    var destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput);

    // Asignar eventos a los botones para calcular la ruta y comenzar la jornada.
    document.getElementById('submit-btn').addEventListener('click', function () {
        calculateRoute();
    });
    document.getElementById('start-journey-btn').addEventListener('click', function () {
        startJourney();
    });
}

// Función para calcular la ruta entre el origen y el destino especificados.
function calculateRoute() {
    // Obtener los valores de origen y destino desde los campos de entrada.
    var originInput = document.getElementById('origin').value;
    var destinationInput = document.getElementById('destination').value;

    // Crear una solicitud de ruta con los puntos de origen y destino, el modo de viaje y opciones adicionales.
    var request = {
        origin: originInput,
        destination: destinationInput,
        travelMode: 'DRIVING', // Modo de viaje (en este caso, en coche)
        provideRouteAlternatives: true // Proporcionar rutas alternativas
    };

    // Enviar la solicitud al servicio de direcciones de Google Maps.
    directionsService.route(request).then(result => {
        // Mostrar la ruta calculada en el mapa.
        directionsDisplay.setDirections(result);
        // Mostrar el botón para iniciar la jornada y habilitarlo.
        document.getElementById('start-journey-btn').style.display = 'block';
        journeyInProgress = true;
        document.getElementById('start-journey-btn').disabled = false;

        // Crear marcadores para el punto de origen y destino de la ruta.
        originPoint = new google.maps.Marker({
            position: result.routes[0].legs[0].start_location,
            map: map,
            icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        });
        destinationPoint = new google.maps.Marker({
            position: result.routes[0].legs[0].end_location,
            map: map,
            icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        });

        // Mostrar información de la ruta (distancia, duración, tarifa estimada) en la interfaz.
        var route = result.routes[0];
        var leg = route.legs[0];
        var distance = leg.distance.value / 1000; // Convertir a kilómetros
        var duration = leg.duration.value / 60; // Convertir a minutos
        var fare = calculateFare(distance, duration); // Calcular la tarifa estimada

        document.getElementById('trip-origin').textContent = leg.start_address;
        document.getElementById('trip-destination').textContent = leg.end_address;
        document.getElementById('trip-distance').textContent = distance.toFixed(2) + ' km';
        document.getElementById('trip-duration').textContent = duration.toFixed(2) + ' mins';
        document.getElementById('trip-fare').textContent = '$' + fare.toFixed(2);

        // Mostrar la información de la ruta en la interfaz.
        document.getElementById('trip-info').style.display = 'block';
    }).catch(error => {
        // Manejar errores en el cálculo de la ruta.
        alert('Error al calcular la ruta: ' + error);
    });
}

// Función para iniciar la jornada simulada siguiendo la ruta calculada.
function startJourney() {
    // Verificar si la jornada está en progreso.
    if (!journeyInProgress) return;

    // Obtener la ruta de la visualización de direcciones.
    var route = directionsDisplay.getDirections().routes[0];
    if (!route || !route.legs || route.legs.length === 0 || !route.legs[0].steps || route.legs[0].steps.length === 0) {
        console.error('No se pudo obtener la ruta o la ruta no tiene pasos.');
        return;
    }

    // Obtener los pasos de la ruta.
    var steps = route.legs[0].steps;
    stepIndex = 0;

    // Crear un marcador para simular el movimiento durante la jornada.
    journeyMarker = new google.maps.Marker({
        position: steps[0].start_location,
        map: map,
        icon: {
            url: '/static/car.png', // Ícono del vehículo
            scaledSize: new google.maps.Size(50, 50) // Tamaño del ícono
        }
    });

    // Limpiar la tabla de instrucciones antes de mostrar nuevas instrucciones.
    document.getElementById('instructions-table').getElementsByTagName('tbody')[0].innerHTML = '';

    // Mostrar las instrucciones de la ruta en la tabla.
    steps.forEach(function(step, index) {
        var instruction = step.instructions;
        var distance = step.distance.text;
        addInstructionToTable(index + 1, instruction, distance);
    });

    // Agregar el punto de partida y el punto de llegada a la tabla de instrucciones.
    addInstructionToTable(0, 'Salida', '');
    addInstructionToTable(steps.length + 1, 'Llegada', '');

    // Simular el movimiento del marcador durante la jornada.
    moveJourneyMarker(steps);
    // Ocultar el botón de inicio de jornada.
    document.getElementById('start-journey-btn').style.display = 'none';
    // Mostrar el estado de la jornada como "¡En marcha!".
    document.getElementById('status').textContent = '¡En marcha!';
    // Mostrar los botones para confirmar la entrega o posponerla.
    document.getElementById('delivered-btn').style.display = 'none';
    document.getElementById('postpone-btn').style.display = 'none';
    // Mostrar la tabla de instrucciones.
    document.getElementById('instructions-table').style.display = 'table';
}

// Función para mover el marcador durante la jornada, simulando el recorrido paso a paso.
function moveJourneyMarker(steps) {
    var step = steps[stepIndex];
    if (!step) return;

    var path = step.path;
    var currentStep = 0;

    // Función recursiva para mover el marcador a lo largo de la ruta.
    function moveMarker() {
        if (currentStep >= path.length) {
            // Si se ha alcanzado el final de la ruta, mostrar los botones de entrega y posposición.
            stepIndex++;
            if (stepIndex < steps.length) {
                setTimeout(() => {
                    moveJourneyMarker(steps);
                }, 1000);
            } else {
                // Si se ha completado la jornada, mostrar los botones de entrega y posposición.
                document.getElementById('delivered-btn').style.display = 'block';
                document.getElementById('postpone-btn').style.display = 'block';
                // Actualizar el estado de la jornada.
                document.getElementById('status').textContent = 'Entrega en progreso...';
            }
            return;
        }

        // Mover el marcador a la siguiente posición en el camino.
        journeyMarker.setPosition(path[currentStep]);
        currentStep++;
        setTimeout(moveMarker, 100); // Llamar recursivamente después de un breve intervalo.
    }

    moveMarker(); // Iniciar el movimiento del marcador.
}

// Función para agregar una instrucción a la tabla de instrucciones.
function addInstructionToTable(stepNumber, instruction, distance) {
    var tbody = document.getElementById('instructions-table').getElementsByTagName('tbody')[0];
    var row = tbody.insertRow(); // Insertar una nueva fila en la tabla.
    var stepCell = row.insertCell(0); // Celda para el número de paso.
    var instructionCell = row.insertCell(1); // Celda para la instrucción.
    var distanceCell = row.insertCell(2); // Celda para la distancia.

    // Asignar contenido a las celdas.
    stepCell.textContent = 'Paso ' + stepNumber;
    instructionCell.innerHTML = instruction;
    distanceCell.textContent = distance;
}

// Función para calcular la tarifa estimada del viaje.
function calculateFare(distance, duration) {
    var baseFare = 50; // Tarifa base del viaje.
    var costPerKm = 10; // Costo por kilómetro.
    var costPerMinute = 2; // Costo por minuto.

    // Calcular la tarifa total sumando la tarifa base, el costo por kilómetro y el costo por minuto.
    return baseFare + (costPerKm * distance) + (costPerMinute * duration);
}

// Event listener para los elementos con clase 'star' (estrellas) para registrar la calificación del viaje.
document.querySelectorAll('.star').forEach(star => {
    star.addEventListener('click', function() {
        var value = this.getAttribute('data-value');
        // Remover la clase 'selected' de todas las estrellas y agregarla a las estrellas seleccionadas.
        document.querySelectorAll('.star').forEach(s => s.classList.remove('selected'));
        for (var i = 0; i < value; i++) {
            document.querySelectorAll('.star')[i].classList.add('selected');
        }
        // Mostrar un mensaje de agradecimiento con la calificación seleccionada.
        alert('Gracias por calificar con ' + value + ' estrellas');
    });
});

// Event listener para el botón de entrega.
document.getElementById('delivered-btn').addEventListener('click', function() {
    // Ocultar los botones de entrega y posposición, y el estado de la jornada.
    document.getElementById('delivered-btn').style.display = 'none';
    document.getElementById('postpone-btn').style.display = 'none';
    document.getElementById('status').textContent = '';
    // Mostrar la sección para calificar el viaje.
    document.getElementById('rating-section').style.display = 'block';
});

