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