import pytest
import jinja2 
import impact
from pathlib import Path

@pytest.mark.parametrize(
    ("params", "expected_diameter"),
    [
        ({"diam": "2", "diameterUnits": "km"}, 2000),
        ({"diam": "10", "diameterUnits": "ft"}, 3.048),
        ({"diam": "", "diameterSelect": "500"}, 500),
        ({"diam": "invalid", "diameterUnits": "m"}, 0),
    ],
)
def test_get_impactor_diameter(params, expected_diameter):
    assert impact.get_impactor_diameter(params) == pytest.approx(expected_diameter)


def test_calc_energy():
    results = impact.calc_energy(
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

def test_calc_energy_gets_impact_energy():
    results = impact.calc_energy(
        pdiameter=320,  # diameter in meters
        pdensity=1000,  # density in kg/m^3
        vInput=50,      # initial velocity in km/s
        velocity=15,    # final velocity in km/s
        theta=45,       # impact angle in degrees
        depth=0,
        distance=1000
    )
    assert 'energy_joules' in results
    assert pytest.approx(2.1e+19, rel=0.1) == results['energy_joules']


def test_airblast_radius_crater():
    radius, airblast = impact.airblast_radius_crater(1000, 1500, 500, False, 100) 
    assert radius > 0
    assert airblast

def test_find_crater():
    crater_results = impact.find_crater(
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
   
def test_find_crater_in_water():
    crater_results = impact.find_crater(
        theta=45,
        depth=50,
        mass=17157284678.805058,
        target_density=1000,
        pdiameter=320,
        velocity=50,
        vseafloor=10,
        dispersion=50,
        energy_seafloor=1e15
    )

    assert pytest.approx(7732, rel=0.1) == crater_results["wdiameter"]
   
def test_atmospheric_entry():
    results = impact.atmospheric_entry(
        pdensity=3000,
        pdiameter=100,
        theta=45,
        vInput=20
    )
    assert 'residual_velocity' in results
    assert pytest.approx(7.742, rel=0.01) == results['residual_velocity']

    assert 'altitudeBurst' in results
    assert pytest.approx(-3114.06, rel=0.1) == results['altitudeBurst']
    assert results['altitudeBurst'] 

    assert 'dispersion' in results
    assert pytest.approx(576.037, rel=0.1) == results['dispersion']


def test_velocity_after_burst():
    results = impact.atmospheric_entry(
        pdensity=1000,
        pdiameter=320,
        theta=45,
        vInput=50
    )
    assert 'residual_velocity' in results
    assert pytest.approx(36.4, rel=0.01) == results['residual_velocity']


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

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(test_data_dir)
    )
    env.filters['scientific'] = lambda v: v  # simple filter for testing
    rendered = env.get_template("Energy.html").render(context)

    assert "Energy Before Atmospheric Entry" in rendered
    assert "1000000000.0 Joules" in rendered
    assert " = 0.00023900573613766732 KiloTons TNT" in rendered
    assert "The average interval between impacts of this size somewhere on Earth is" in rendered
    assert "<b>20.0 years.</b>" in rendered

def test_atmospheric_entry_display():
    test_data_dir = Path(__file__).parent.parent / "templates"

    # assume it is an unittest function
    context = {  # your variables to pass to template
        'iFactor': 0.8,
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
    assert impact.orbit_impact(0.0005) == "Negligible"
    assert impact.orbit_impact(0.2) == "Total"    
    assert impact.orbit_impact(0.005) == "Noticeable"    
    assert impact.orbit_impact(0.05) == "Substantial"


def test_calculate_dispersion_ellipse():
    a, b = impact.calculate_dispersion_ellipse(
        dispersion=1059,
        theta=45
    )
    assert pytest.approx(1.5, rel=0.01) == a
    assert pytest.approx(1.06, rel=0.01) == b


def test_calculate_lost_energy():
    lost_energy = impact.calculate_lost_energy(
        mass=100,
        entry_vkm=50,
        ending_vkm=30
    )
    assert lost_energy == 80000000000.0


def test_airblast_radius_crater():
    radius, airblast = impact.airblast_radius_crater(
        energy_ktons=1e15,
        rkt=1500,
        altitudeBurst=2000,
        CraterRadiusFinal=500,
        qCrater=True
    )
    assert radius > 0
    assert airblast


def test_find_airblast():
    airblast = impact.find_airblast(
        energy_ktons=1e15,
        altitudeBurst=2000,
        qCrater=True,
        CraterRadiusFinal=500
    )
    assert len(airblast) == 4


def test_air_blast():
    airblast = impact.air_blast(
        energy_blast=1e15,
        distance=100,
        altitudeBurst=2000
    )
    assert airblast['shock_arrival'] > 0
    assert airblast['opressure'] > 0
    assert airblast['vmax'] > 0

def test_find_thermal():
    thermal = impact.find_thermal(
        energy_megatons=1e15,
        energy_surface=2000
    )
    assert len(thermal) == 3

@pytest.mark.parametrize(
    ("effective_threshold", "first_mercalli", "labels"),
    [
        (9, 10, (10, 11, 12)),
        (8, 10, (10, 11)),
        (7, 9, (9, 10)),
        (6, 7, (7, 8)),
        (5, 6, (6, 7)),
        (4, 4, (4, 5)),
        (3, 3, (3, 4)),
        (2, 1, (1, 2)),
    ],
)
def test_mercalli_levels(effective_threshold, first_mercalli, labels):
    levels = impact.mercalli_levels(effective_threshold)

    assert isinstance(levels, tuple)
    actual_first_mercalli, descriptions = levels
    assert actual_first_mercalli == first_mercalli
    assert isinstance(descriptions, tuple)
    assert descriptions == tuple(
        impact.MERCALLI_DESCRIPTIONS[label - 1] for label in labels
    )


def test_calculate_seismic_effects():
    effects = impact.calculate_seismic_effects(energy_seafloor=1e15, distance_km=100)

    assert effects["richter_magnitude"] == pytest.approx(4.18)
    assert effects["seismic_arrival"] == pytest.approx(20)
    assert effects["intensity_descriptions"][0].startswith("Not felt.")

@pytest.mark.parametrize(
    ("effective_magnitude", "first_mercalli", "descriptions"),
    [
        (1.1, 1, ("Nothing would be felt",)),
        (2.1, 1, ("Not felt.", "Felt by persons at rest")),
        (3.1, 3, ("Felt quite noticeably", "Hanging objects swing")),
        (4.1, 4, ("Hanging objects swing", "Felt outdoors")),
        (5.1, 6, ("Felt by all", "Difficult to stand")),
        (6.1, 7, ("Difficult to stand", "Steering of motor cars affected")),
        (7.1, 9,("General panic", "Large landslides")),
        (8.1, 10, ("Large landslides", "Rails bent greatly")),
        (9.1, 10, ("Large landslides", "Rails bent greatly", "Damage nearly total")),
    ],
)
def test_calculate_seismic_effects_uses_mercalli_levels(
    effective_magnitude, first_mercalli, descriptions
):
    distance_km = 100
    magnitude = effective_magnitude + 0.0048 * distance_km + 2.5644 - 1.4
    energy_seafloor = 10 ** ((magnitude + 5.87) / 0.67)

    effects = impact.calculate_seismic_effects(energy_seafloor, distance_km)

    assert effects["mercalli_start"] == first_mercalli

    assert len(effects["intensity_descriptions"]) == len(descriptions)
    for expected, actual in zip(descriptions, effects["intensity_descriptions"]):
        assert expected in actual



def test_calculate_seismic_effects_requires_positive_distance():
    with pytest.raises(ValueError, match="distance_km must be greater than zero"):
        impact.calculate_seismic_effects(energy_seafloor=1e15, distance_km=0)

def test_calculate_thermal_effects():
    effects = impact.calculate_thermal_effects(
        energy_surface=1e15,
        energy_megatons=1e15 / (4.186 * 10**15),
        distance_km=10,
        velocity=20
    )

    assert effects["status"] == "visible"
    assert effects["thermal_exposure"] == pytest.approx(4536.12)
    assert effects["damage_descriptions"] == []

def test_calculate_thermal_effects_conditions():
    assert impact.calculate_thermal_effects(1e15, 1, 10, 14)["status"] == "no_fireball"
    assert impact.calculate_thermal_effects(1e15, 1, 1000, 20)["status"] == "below_horizon"

def test_calculate_thermal_effects_requires_positive_distance():
    with pytest.raises(ValueError, match="distance_km must be greater than zero"):
        impact.calculate_thermal_effects(1e15, 1, 0, 20)

def test_ejecta_radius():
    radius = impact.ejecta_radius(
        EjectaThickness=1,
        Dtr=1e8,
        CraterRadiusTransient=300,
        CraterRadiusFinal=500
    )
    assert radius == 500

def test_calculate_ejecta_effects():
    effects = impact.calculate_ejecta_effects(
        distance_km=100,
        Dtr=10000,
        cdiameter=12500
    )

    assert effects["ejecta_arrival"] == pytest.approx(144.169, rel=1e-3)
    assert effects["ejecta_thickness"] == pytest.approx(0.0892857)
    assert effects["d_frag"] == pytest.approx(0.079427, rel=1e-3)

def test_calculate_ejecta_effects_requires_positive_distance():
    with pytest.raises(ValueError, match="distance_km must be greater than zero"):
        impact.calculate_ejecta_effects(distance_km=0, Dtr=10000, cdiameter=12500)

def test_seismic_radius():
    radius = impact.seismic_radius(
        mag = 5,
        mag_eff=3,
        CraterRadiusFinal=1000
    )
    assert radius > 0

def test_tsunami_radius():
    radius = impact.tsunami_radius(
        Rmax=1000,
        Rexp=2,
        A=10,
        Amax=50,
        CraterRadiusFinal=300
    )
    assert radius > 0
