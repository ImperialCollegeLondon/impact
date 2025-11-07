from flask import Flask, render_template, request
from impact import get_location

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ImpactEffects')
def impact_effects():
    locations = ["London", "Los Angeles", "New York", "Berlin", "Paris", "Johannesburg", "Sydney"]
    craters = ["Acraman (Australia)", "Araguainha (Brazil)", "Barringer (USA)", "Chicxulub (Mexico)", "Chesapeake Bay (USA)", "Eltanin (Bellingshausen Sea)", "Popiagai (Russia)", "Ries (Germany)", "Siljan (Sweden)", "Sudbury (Canada)", "Vredefort (South Africa)"]
    return render_template('ImpactEffects.html', locations=sorted(locations), craters=sorted(craters))

@app.route('/map')
def map_page():
    return render_template('map.html', location=get_location(request.args))

if __name__ == '__main__':
    app.run(debug=True)
