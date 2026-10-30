import pytest

from main import app


@pytest.mark.parametrize('legacy_url', [
    '/ImpactEarth/ImpactEffects',
    '/ImpactEarth/ImpactEffects/',
])
def test_legacy_impact_effects_url_redirects_to_canonical_url(legacy_url):
    app.config.update(TESTING=True)

    with app.test_client() as client:
        response = client.get(legacy_url, follow_redirects=False)

    assert response.status_code == 308
    assert response.headers['Location'] == '/ImpactEffects'


def test_distance_results_include_thermal_and_seismic_effects():
    app.config.update(TESTING=True)

    with app.test_client() as client:
        response = client.get(
            '/map?diam=100&diameterUnits=m&pdens=3000&vel=17&theta=45'
            '&distance=100&distanceUnits=km'
        )

    assert response.status_code == 200
    assert b'Thermal Radiation:' in response.data
    assert b'Seismic Effects:' in response.data