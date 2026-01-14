function add_airblast(groundzero, airblastRadii, map ) {
    var label_A = ["Glass window damage (1 kPa)","Glass windows shatter (5 kPa)","Wood-frame buildings collapse (20 kPa)","Steel-framed buildings collapse","Vehicles overturned and distorted"];

    var airblastLayer = L.layerGroup();

    airblastLayer.addTo(map);
    
    airblastRadii.slice().reverse().forEach(function(radius, idx) {
        var airblastCircle = L.circle(groundzero, {
            radius: radius*1.274E7*0.5,
            color: 'blue',
            fillColor: 'blue',
            fillOpacity: 0.25,
            weight: 1
        })

        airblastCircle.on('mouseover', function (e) {
            var popup = L.popup()
                .setLatLng(e.latlng)
                .setContent(label_A[idx] + ": " + (radius*1.274E7*0.5).toLocaleString() + " meters")
                .openOn(map);
        });
        airblastCircle.on('mouseout', function (e) {
            map.closePopup();
        });

        airblastLayer.addLayer(airblastCircle);
    });
    
    L.control.layers(null, { "Airblast": airblastLayer }).addTo(map);
}

function add_fireball(groundzero, fireballRadii, map ) {
    var fireballLayer = L.layerGroup();
    fireballLayer.addTo(map);

    // Find existing layer control, if any, and add Fireball layer to it
    var existingControl = null;
    map.eachLayer(function(layer) {
        if (layer instanceof L.Control.Layers) {
            existingControl = layer;
        }
    });

    if (existingControl) {
        existingControl.addOverlay(fireballLayer, "Fireball");
    } else {
        L.control.layers(null, { "Fireball": fireballLayer }).addTo(map);
    }
}