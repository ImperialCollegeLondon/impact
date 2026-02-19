document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([40, 25], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    var marker;
    map.on('click', function(e) {
        var lat = e.latlng.lat.toFixed(6);
        var lon = e.latlng.lng.toFixed(6);
        document.getElementById('latitude').value = lat;
        document.getElementById('longitude').value = lon;
        if (marker) {
            marker.setLatLng(e.latlng);
        } else {
            marker = L.marker(e.latlng).addTo(map);
        }
    });

    function updateMapView() {
        var lat = parseFloat(document.getElementById('latitude').value);
        var lon = parseFloat(document.getElementById('longitude').value);
        if (!isNaN(lat) && !isNaN(lon)) {
            map.setView([lat, lon], map.getZoom());
            if (marker) {
                marker.setLatLng([lat, lon]);
            } else {
                marker = L.marker([lat, lon]).addTo(map);
            }
        }
    }
    document.getElementById('latitude').addEventListener('change', updateMapView);
    document.getElementById('longitude').addEventListener('change', updateMapView);

    Array.from(document.getElementsByClassName('specificLocation')).forEach(function(select) {
        select.addEventListener('change', function() {
            var selectedIndex = this.selectedIndex;
            if (selectedIndex > 0) {
                var coords = this.value.split(",");
                if (coords.length === 2) {
                    var loc = { lat: coords[0], lon: coords[1] };
                    if (loc.lat !== undefined && loc.lon !== undefined) {
                        document.getElementById('latitude').value = loc.lat;
                        document.getElementById('longitude').value = loc.lon;
                        updateMapView();
                    }
                }
            }
        });
    });

    document.getElementById('distanceonly').addEventListener('change', function() {
        var disabled = this.checked;
        Array.from(document.getElementsByClassName('specificLocation')).forEach(function(select) {
            select.disabled = disabled;
        });
        document.getElementById('latitude').disabled = disabled;
        document.getElementById('longitude').disabled = disabled;
        document.getElementById('map').style.pointerEvents = disabled ? 'none' : 'auto';
        document.getElementById('map').style.opacity = disabled ? '0.5' : '1';

        document.getElementsByName('distance')[0].disabled = !disabled;
        document.getElementsByName('distanceUnits')[0].disabled = !disabled;
    });

    document.getElementById('diameterSelect').addEventListener('change', function() {
        // Update diameter value when changed
        document.getElementById('diameter').value = this.value;
    });

    document.getElementById('densitySelect').addEventListener('change', function() {
        // Update density value when changed
        document.getElementById('density').value = this.value;
    });

    document.getElementById('velsel').addEventListener('change', function() {
        document.getElementById('vel').value = this.value;
        document.getElementById('velUnits').value = "1"; // Set to km/s when a velocity is selected from the list
    });

    document.getElementById('angle_select').addEventListener('change', function() {
        // Update angle value when changed
        document.getElementById('theta').value = this.value;
    });

    document.getElementById('submit').addEventListener('click', function(e) {
        var lat = document.getElementById('latitude').value;
        var lon = document.getElementById('longitude').value;
        var distanceOnly = document.getElementById('distanceonly').checked;
        
        hasErrors = false;
        if (!distanceOnly && (!lat || !lon)) {
            e.preventDefault();
            var errorElement = document.getElementById('latlong-error');
            errorElement.textContent = 'Please select a location on the map or enter latitude and longitude.';
            hasErrors = true;
        }

        var distance = document.getElementsByName('distance')[0].value;
        var distanceUnits = document.getElementsByName('distanceUnits')[0].value;
        if (distanceOnly && (!distance || isNaN(distance) || distance <= 0)) {
            e.preventDefault();
            var errorElement = document.getElementById('distance-error');
            errorElement.textContent = 'Please enter a valid positive number for distance.';
            hasErrors = true;
        }


        var velocity = document.getElementById('vel').value;
        var velocityUnits = document.getElementById('velUnits').value;
        if (!velocity || isNaN(velocity) || velocity <= 0) {
            e.preventDefault();
            var errorElement = document.getElementById('velocity-error');
            errorElement.textContent = 'Please enter a valid positive number for velocity.';
            hasErrors = true;
        }

        var angle = document.getElementById('theta').value;
        if (!angle || isNaN(angle) || angle < 0 || angle > 90) {
            e.preventDefault();
            var errorElement = document.getElementById('angle-error');
            errorElement.textContent = 'Please enter a valid angle between 0 and 90 degrees.';
            hasErrors = true;
        }

        var diameter = document.getElementById('diameter').value;
        if (!diameter || isNaN(diameter) || diameter <= 0) {
            e.preventDefault();
            var errorElement = document.getElementById('diameter-error');
            errorElement.textContent = 'Please enter a valid positive number for diameter.';
            hasErrors = true;
        }

        var density = document.getElementById('density').value;
        if (!density || isNaN(density) || density <= 0) {
            e.preventDefault();
            var errorElement = document.getElementById('density-error');
            errorElement.textContent = 'Please enter a valid positive number for density.';
            hasErrors = true;
        }

        var targetTypeSelected = document.querySelector('input[name="target_type"]:checked');
        if (!targetTypeSelected) {
            e.preventDefault();
            var errorElement = document.getElementById('target-error');
            errorElement.textContent = 'Please select a target type.';
            hasErrors = true;
        }

        var waterChecked = document.querySelector('input[name="target_type"][value="water"]:checked');
        if (waterChecked) {
            var depthValue = document.getElementById('depth').value;
            if (!depthValue || isNaN(depthValue) || depthValue <= 0) {
                e.preventDefault();
                var errorElement = document.getElementById('depth-error');
                errorElement.textContent = 'Please enter a valid positive number for depth.';
                hasErrors = true;
            }
        }
        return !hasErrors; // Only submit if there are no errors
    });
});