import pytest
import flask_app.impact

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
    radius, transient_radius = flask_app.impact.find_crater(
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

    assert radius > 0
    assert transient_radius > 0
   

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
    assert results['dispersion'] is None