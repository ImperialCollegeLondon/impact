from main import app


def test_legacy_impact_effects_url_redirects_to_canonical_url():
    app.config.update(TESTING=True)

    with app.test_client() as client:
        response = client.get('/ImpactEarth/ImpactEffects', follow_redirects=False)

    assert response.status_code == 308
    assert response.headers['Location'] == '/ImpactEffects'