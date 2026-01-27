document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([20, 0], 2);
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
});