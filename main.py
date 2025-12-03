from flask import Flask, render_template, request
import impact
import formatters

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ImpactEffects')
def impact_effects():
    locations = ["London", "Los Angeles", "New York", "Berlin", "Paris", "Johannesburg", "Sydney"]
    craters = ["Acraman (Australia)", "Araguainha (Brazil)", "Barringer (USA)", "Chicxulub (Mexico)", "Chesapeake Bay (USA)", "Eltanin (Bellingshausen Sea)", "Popiagai (Russia)", "Ries (Germany)", "Siljan (Sweden)", "Sudbury (Canada)", "Vredefort (South Africa)"]
    density = {
        "1000": "1000 kg/m^3 for ice",
        "1500": "1500 kg/m^3 for porous rock",
        "3000": "3000 kg/m^3 for dense rock",
        "8000": "8000 kg/m^3 for iron"
    }

    diameter_options = {
        "0.25": "Football (25 cm)",
        "5": "Double-decker bus (5 m)",
        "20": "Cricket wicket (20 m)",
        "52.": "Nelson's column (52 m)",
        "87.": "Queen's Tower (87 m)",
        "320.": "Wembley Stadium (320 m)",
        "1340.": "Ben Nevis (1.3 km)",
        "10000.": "Jersey (10 km)",
        "20000.": "Isle of Wight (20 km)",
        "0": "-- Asteroids --",
        # Asteroid options commented out in original
        # "952000.": "Ceres (952 km)",
        # "529000.": "Vesta (529 km)",
        # "100000.": "Lutitia (100 km)",
        # "53000.": "Mathilde (53 km)",
        # "33000.": "Ida (33 km)",
        "500.": "Itokawa (500 m)",
        "325.": "Apophis (325 m)",
        "250.": "Bennu (250 m)",
        "0": "-- Comets --",
        "6300.": "Tempel 1 (6.3 km)",
        "4200.": "67P/Churyumovâ€“Gerasimenko (4.2 km)",
        "4200.": "Wild 2 (4.2 km)",
        "1500.": "Hartley 2 (1.5 km)",
        "0": "-- Past events --",
        "20": "Chelyabinsk (20 m)",
        "50": "Tunguska (50 m; stone)",
        "50": "Barringer (50 m; iron)",
        "1500": "Ries (1.5 km)",
        "14000": "Chicxulub (14 km)"
    }
    return render_template('ImpactEffects.html', 
                           locations=sorted(locations), craters=sorted(craters), pdens_options=density.items(), diameter_options=diameter_options.items())


@app.route('/map')
def map_page():
    distance = request.args.get('distance', '')
    distance_units = request.args.get('distance_units', 'km')
    dist = impact.calculate_distance_km(distance, distance_units)

    try:
        density = float(request.args.get('pdens', ''))
    except ValueError:
        density = float(request.args.get('pdens_select', '0'))

    diameter_meters = impact.get_impactor_diameter(request.args)

    vkm = impact.calculate_velocity_km(request.args.get('vel', ''), request.args.get('velocityUnits', 'km/s'))
    theta = float(request.args.get('theta', '45'))
    depth_meters=impact.get_depth_meters(request.args)

    # Calculate the effects of atmospheric entry
    atmospheric_entry_effects = impact.atmospheric_entry(density, diameter_meters, theta, vkm)

    energy_results = impact.calc_energy(
        pdiameter=diameter_meters,
        pdensity=density,
        vInput=vkm,
        velocity=atmospheric_entry_effects['velocity'],
        theta=theta,
        depth=depth_meters,
        distance=dist
    )

    crater_results = impact.find_crater(theta=theta, 
                        depth=depth_meters,
                        mass=energy_results['mass'], 
                        target_density=float(request.args.get('tdens', '2500')),
                        pdiameter=diameter_meters,
                        velocity=vkm,
                        vseafloor=energy_results['vseafloor'],
                        dispersion=atmospheric_entry_effects['dispersion'], 
                        energy_seafloor=energy_results['energy_seafloor'],
                        )
    
    qCrater = atmospheric_entry_effects['altitudeBurst'] <= 0
    airblast_radii = impact.find_airblast(energy_results['energy_blast'], atmospheric_entry_effects['altitudeBurst'], qCrater, crater_results['CraterRadiusFinal'])

    lost_energy = impact.calculate_lost_energy(energy_results['mass'], vkm, atmospheric_entry_effects["velocity"])
    dispersion_ellipse = impact.calculate_dispersion_ellipse(atmospheric_entry_effects['dispersion'], theta, distance_km=dist)
    return render_template('map.html', location=impact.get_location(request.args), 
                           density=density, distance_km=dist, 
                           velocity_km_per_second=vkm, 
                           diameter_meters=diameter_meters,
                           trot_change=energy_results['trot_change'],
                           impact_angle=theta,
                           depth=depth_meters,
                           ifactor=atmospheric_entry_effects['ifactor'],
                           altitudeBU =atmospheric_entry_effects['altitudeBU'],
                           altitudeBurst=atmospheric_entry_effects['altitudeBurst'],
                           mratio=crater_results['mratio'],
                            lratio=energy_results['lratio'],
                           energy_joules=energy_results['energy0'],
                           rec_time_years=energy_results['rec_time'],
                           target_density=request.args.get('tdens', '2500'),
                           orbit_impact=impact.orbit_impact(energy_results['pratio']),
                           residual_velocity=atmospheric_entry_effects['velocity'],
                           lost_energy_joules=lost_energy,
                           dispersion_ellipse=dispersion_ellipse)



if __name__ == '__main__':
    app.jinja_env.filters['duration'] = formatters.format_duration
    app.jinja_env.filters['scientific'] = formatters.format_scientific
    app.run(debug=True)
