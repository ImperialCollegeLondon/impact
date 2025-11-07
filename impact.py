
def get_location(params):
    # Extract parameters
    latitude = params.get("latitude", "")
    longitude = params.get("longitude", "")
    location = None

    if latitude == "" and longitude == "":
        location = params.get("LocationSelect", None)
        locations_dict = {
            "London": (51.5, -0.125),
            "Los Angeles": (34.052, -118.244),
            "New York": (40.767, -73.975),
            "Berlin": (52.525, 13.4114),
            "Paris": (48.86, 2.35),
            "Johannesburg": (-26.201, 28.045),
            "Sydney": (-33.864, 151.193),
        }
        if location in locations_dict:
            latitude, longitude = locations_dict[location]

    if location == 0:
        craters_dict = {
            "Aracman": (-32.0173, 135.45),
            "Araguainha": (-16.783, -52.983),
            "Barringer": (35.0272, -111.0228),
            "Chicxulub": (21.3, -89.5),
            "Chesapeake Bay": (37.283, -76.017),
            "Eltanin": (-57.787, -90.793),
            "Popigai": (71.65, 111.1833),
            "Ries": (48.883, 10.617),
            "Siljan": (61.0333, 14.87),
            "Sudbury": (46.6, -81.18),
            "Vredefort": (-27.0, 27.5),
        }
        earth_crater = params.get("CraterSelect", None)
        if earth_crater in craters_dict:
            latitude, longitude = craters_dict[earth_crater]

    return latitude, longitude