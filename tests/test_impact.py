import pytest
import jinja2 
import flask_app.impact
from pathlib import Path

def test_calc_energy():
    results = flask_app.impact.calc_energy(
        pdiameter=100,  # diameter in meters
        pdensity=3000,  # density in kg/m^3
        vInput=20,      # initial velocity in km/s
        velocity=15,    # final velocity in km/s
        theta=45,       # impact angle in degrees
        depth=0,
        distance=1000
    )
    assert 'mass' in results
    assert 'vseafloor' in results
    assert 'energy_seafloor' in results
    assert results['mass'] > 0
    assert results['vseafloor'] > 0
    assert results['energy_seafloor'] > 0

def test_airblast_radius_crater():
    radius, airblast = flask_app.impact.airblast_radius_crater(1000, 1500, 500, False, 100) 
    assert radius > 0
    assert airblast

def test_find_crater():
    crater_results = flask_app.impact.find_crater(
        theta=45,
        depth=0,
        mass=1e9,
        target_density=2500,
        pdiameter=100,
        velocity=15,
        vseafloor=10,
        dispersion=50,
        energy_seafloor=1e15
    )

    assert crater_results["CraterRadiusFinal"] > 0
    assert crater_results["CraterRadiusTransient"] > 0
   

def test_atmospheric_entry():
    results = flask_app.impact.atmospheric_entry(
        pdensity=3000,
        pdiameter=100,
        theta=45,
        vInput=20
    )
    assert 'velocity' in results
    assert pytest.approx(2.49, rel=0.01) == results['velocity']

    assert 'altitudeBurst' in results
    assert pytest.approx(2273, rel=0.1) == results['altitudeBurst']
    assert results['altitudeBurst'] 

    assert 'dispersion' in results
    assert results['dispersion'] == 0

def test_mratio_display():
    test_data_dir = Path(__file__).parent.parent / "templates"

    # assume it is an unittest function
    context = {  # your variables to pass to template
        'mratio': 0.156,
        'lratio': 0.3,
        'trot_change': 3661,
        'orbit_impact': 'significant'
    }

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(test_data_dir)
    )

    env.filters['duration'] = lambda s: f"{s} seconds"  # simple filter for testing
    rendered = env.get_template("MajorGlobalChanges.html").render(context)
    assert '<b>15.6</b> percent of the Earth is melted by the impact' in rendered
    assert "the impact may make a significant change in the tilt of Earth's axis" in rendered
    assert "The Earth is not strongly disturbed by the impact and loses negligible mass." in rendered

def test_energy_display():
    test_data_dir = Path(__file__).parent.parent / "templates"

    # assume it is an unittest function
    context = {  # your variables to pass to template
        'energy_joules': 1e9,
        'rec_time_years': 20,
    }

    rendered = jinja2.Environment(
        loader=jinja2.FileSystemLoader(test_data_dir)
    ).get_template("Energy.html").render(context)

    assert "Energy before atmospheric entry: 1.00e+09 Joules" in rendered
    assert " = 2.39e-04 Kilotons of TNT" in rendered
    assert "The average interval between impacts of this size somewhere on Earth is" in rendered
    assert "<b>20.0 years.</b>" in rendered

def test_atmospheric_entry_display():
    test_data_dir = Path(__file__).parent.parent / "templates"

    # assume it is an unittest function
    context = {  # your variables to pass to template
        'ifactor': 0.8,
        'altitudeBurst': 5000,
        'altitudeBU': 8000,
        'density': 3000,
        'residual_velocity': 8.2,
        'energy_joules': 1.75e14,
    }

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(test_data_dir)
    )
    
    env.filters['scientific'] = lambda v: v  # simple filter for testing
    rendered = env.get_template("AtmosphericEntry.html").render(context)

    print(rendered)
    assert "The projectile begins to breakup at an altitude of <b>8000 meters = 26246 ft</b>" in rendered
    assert "The projectile bursts into a cloud of fragments at an altitude of <b>5000 meters = 16404 ft</b>" in rendered
    assert "The residual velocity of the projectile fragments after the burst is <b>8.2 km/s = 5.1 miles/s</b>" in rendered
    assert "The energy of the airburst is 175000000000000.0 Joules = 0.04 MegaTons" in rendered

def test_daylength_change():
    test_data_dir = Path(__file__).parent.parent / "templates"

    context = {  # your variables to pass to template
        'mratio': 0.156,
        'lratio': 0.3,
        'trot_change': 3661,
    }

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(test_data_dir)
    )
    env.filters['duration'] = lambda s: f"{s} seconds"  # simple filter for testing

    rendered = env.get_template("MajorGlobalChanges.html").render(context)

    assert "the day of up to <b>3661 seconds</b>." in rendered

def test_orbit_impact():
    assert flask_app.impact.orbit_impact(0.0005) == "Negligible"
    assert flask_app.impact.orbit_impact(0.2) == "Total"    
    assert flask_app.impact.orbit_impact(0.005) == "Noticeable"    
    assert flask_app.impact.orbit_impact(0.05) == "Substantial"

def test_calculate_dispersion_ellipse():
    a, b = flask_app.impact.calculate_dispersion_ellipse(
        dispersion=100,
        distance_km=20,
        theta=45
    )
    assert a > 0
    assert b > 0

def test_calculate_lost_energy():
    lost_energy = flask_app.impact.calculate_lost_energy(
        mass=100,
        entry_vkm=50,
        ending_vkm=30
    )
    assert lost_energy == 80000000000.0
