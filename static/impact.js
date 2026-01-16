function add_airblast(groundzero, airblastRadii, map ) {
    var label_A = ["Glass window damage (1 kPa)","Glass windows shatter (5 kPa)","Wood-frame buildings collapse (20 kPa)","Steel-framed buildings collapse","Vehicles overturned and distorted"];

    var airblastLayer = L.layerGroup();

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
    return airblastLayer;
}

function add_fireball(groundzero, fireballRadii, map ) {
    var fireballLayer = L.layerGroup();

    fireballRadii.slice().reverse().forEach(function(radius, idx) {
        var blastCircle = L.circle(groundzero, {
            radius: radius*1.274E7*0.5,
            color: 'red',
            fillColor: 'red',
            fillOpacity: 0.25,
            weight: 1
        })

        var label_F = ["Fireball Visible","Clothing Ignites","Fireball"];
        blastCircle.on('mouseover', function (e) {
            var popup = L.popup()
                .setLatLng(e.latlng)
                .setContent(label_F[idx] + ": " + (radius*1.274E7*0.5).toLocaleString() + " meters")
                .openOn(map);
        });
        blastCircle.on('mouseout', function (e) {
            map.closePopup();
        });

        fireballLayer.addLayer(blastCircle);
    });
    return fireballLayer
}

function add_ejecta(groundzero, ejectaRadii, map ) {
    var label_E = ["Ejecta thickness > 1 cm","Ejecta thickness > 10 cm","Ejecta thickness > 1 m","Ejecta thickness > 10 m","Ejecta thickness > 100 m"];

    var ejectaLayer = L.layerGroup();

    ejectaRadii.forEach(function(radius, idx) {
        var ejectaCircle = L.circle(groundzero, {
            radius: radius[1]*1.274E7*0.5,
            color: 'skyblue',
            fillColor: 'skyblue',
            fillOpacity: 0.25,
            weight: 1
        })

        ejectaCircle.on('mouseover', function (e) {
            var popup = L.popup()
                .setLatLng(e.latlng)
                .setContent(label_E[idx] + ": " + (radius[1]*1.274E7*0.5).toLocaleString() + " meters")
                .openOn(map);
        }
        );
        ejectaCircle.on('mouseout', function (e) {
            map.closePopup();
        });

        ejectaLayer.addLayer(ejectaCircle);
    });
    return ejectaLayer;
}

function add_seismic(groundzero, seismicRadii, map ) {
    var label_S = ["Mercalli Intensity III; Vibration like passing of light trucks.",
        "Mercalli Intensity V; Small unstable objects displaced.",
        "Mercalli Intensity VII; Difficult to stand; landslides; damage to buildings.",
        "Mercalli Intensity IX",
        "Mercalli Intensity XII"];

    var seismicLayer = L.layerGroup();

    seismicRadii.forEach(function(radius, idx) {
        var seismicCircle = L.circle(groundzero, {
            radius: radius[1]*1.274E7*0.5,
            color: 'green',
            fillColor: 'green',
            fillOpacity: 0.25,
            weight: 1
        })

        seismicCircle.on('mouseover', function (e) {
            var popup = L.popup()
                .setLatLng(e.latlng)
                .setContent(label_S[idx] + ": " + (radius[1]*1.274E7*0.5).toLocaleString() + " meters")
                .openOn(map);
        }
        );
        seismicCircle.on('mouseout', function (e) {
            map.closePopup();
        });

        seismicLayer.addLayer(seismicCircle);
    });
    return seismicLayer;
}


function add_tsunami(groundzero, tsunamiRadii, map ) {
        var label_T = ["Tsunami wave height > 1 m", 
            "Tsunami wave height > 10 m",
            "Tsunami wave height > 100 m",
            "Tsunami wave height > 1 km"];

    var tsunamiLayer = L.layerGroup();

    tsunamiRadii.forEach(function(radius, idx) {
        var tsunamiCircle = L.circle(groundzero, {
            radius: radius[1]*1.274E7*0.5,
            color: 'cyan',
            fillColor: 'cyan',
            fillOpacity: 0.25,
            weight: 1
        })

        tsunamiCircle.on('mouseover', function (e) {
            var popup = L.popup()
                .setLatLng(e.latlng)
                .setContent(label_T[idx] + ": " + (radius[1]*1.274E7*0.5).toLocaleString() + " meters")
                .openOn(map);
        }
        );
        tsunamiCircle.on('mouseout', function (e) {
            map.closePopup();
        });

        tsunamiLayer.addLayer(tsunamiCircle);
    });
    return tsunamiLayer;
}

function add_crater(groundzero, craterRadii, map ) {
    var label_C = ['Final Crater','Transient Crater'];

    var craterLayer = L.layerGroup();

    craterRadii.forEach(function(radius, idx) {
        var craterCircle = L.circle(groundzero, {
            radius: radius*1.274E7*0.5,
            color: 'white',
            fillColor: 'white',
            fillOpacity: 0.25,
            weight: 1
        })

        craterCircle.on('mouseover', function (e) {
            var popup = L.popup()
                .setLatLng(e.latlng)
                .setContent(label_C[idx] + ": " + (radius*1.274E7*0.5).toLocaleString() + " meters")
                .openOn(map);
        }
        );
        craterCircle.on('mouseout', function (e) {
            map.closePopup();
        });

        craterLayer.addLayer(craterCircle);
    });
    return craterLayer;
}

