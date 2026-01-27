import math
from collections import namedtuple

EARTH_RADIUS_KM = 6371.0
EARTH_ANGULAR_MOMENTUM = 5.86 * 10**33;		# (kg m^3)/sec
EARTH_MASS = 5.97 * 10**24             # Mass of Earth in kg
EARTH_VOLUME = 1.1 * 10**12		# volume of earth in km^3
EARTH_LINEAR_MOMENTUM = 1.794 * 10**32  # linear momentum of earth in (kg * m) / sec
RHO_SURFACE = 1			# surface density of atmosphere kg/m^3
PANCAKE_FACTOR = 7.0
G = 9.8            		# acceleration due to gravity
DRAG_COEFFICIENT = 2	# drag coefficient
MELT_COEFFICIENT = 8.9 * 10**-21		# coefficient for melt volume calc
SCALE_HEIGHT = 8000			# scale height of atmosphere in m
PO = 10**5;				# ambient pressure in Pa

def get_cities():
    City = namedtuple('City', ['name', 'lat', 'long'])
    cities = [
        City("London", 51.5, -0.125),
        City("Los Angeles", 34.052, -118.244),
        City("New York", 40.767, -73.975),
        City("Berlin", 52.525, 13.4114),
        City("Paris", 48.86, 2.35),
        City("Johannesburg", -26.201, 28.045),
        City("Sydney", -33.864, 151.193),
    ]
    return cities

def get_craters():
    Crater = namedtuple('Crater', ['name', 'lat', 'long'])
    craters = [
        Crater("Acraman (Australia)", -32.0173, 135.45),
        Crater("Araguainha (Brazil)", -16.783, -52.983),
        Crater("Barringer (USA)", 35.0272, -111.0228),
        Crater("Chicxulub (Mexico)", 21.3, -89.5),
        Crater("Chesapeake Bay (USA)", 37.283, -76.017),
        Crater("Eltanin (Bellingshausen Sea)", -57.787, -90.793),
        Crater("Popiagai (Russia)", 71.65, 111.1833),
        Crater("Ries (Germany)", 48.883, 10.617),
        Crater("Siljan (Sweden)", 61.0333, 14.87),
        Crater("Sudbury (Canada)", 46.6, -81.18),
        Crater("Vredefort (South Africa)", -27.0, 27.5),
    ]
    return craters

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


def get_impactor_diameter(params):
    # Get diameter and units
    pdiameter = params.get("diam", "")
    punits = params.get("diameterUnits", None)
    if pdiameter == "":
        pdiameter = params.get("diameterSelect", "")
        punits = 1

    try:
        pdiameter = float(pdiameter)
    except (TypeError, ValueError):
        pdiameter = 0

    if punits == 2:
        pdiameter *= 1000  # kilometers to meters
    elif punits == 3:
        pdiameter *= 0.3048  # feet to meters
    elif punits == 4:
        pdiameter *= 1609.34  # miles to meters

    return pdiameter


def get_depth_meters(params):
    depth = params.get("wdepth", "")
    depth_units = params.get("wdepthUnits", "meters")
    try:
        depth_value = float(depth)
    except (TypeError, ValueError):
        depth_value = 0.0

    if depth_units == 'feet':
        depth_meters = depth_value * 0.3048
    else:
        depth_meters = depth_value

    return depth_meters


def calculate_distance_km(distance, distance_units):
    try:
        distance_value = float(distance)
    except (TypeError, ValueError):
        distance_value = 0.0

    if distance_units == 'miles':
        distance_km = distance_value * 1.60934
    else:
        distance_km = distance_value

    return distance_km


def calculate_velocity_km(vel, velocity_units):
    try:
        velocity_value = float(vel)
    except (TypeError, ValueError):
        velocity_value = 0.0

    if velocity_units == 'miles/s':
        velocity_km = velocity_value * 1.60934
    else:
        velocity_km = velocity_value
    return velocity_km



def airblast_radius_crater(
    energy_ktons: float,
    rkt: float,
    altitudeBurst: float,
    qCrater: bool,
    CraterRadiusFinal: float
) -> tuple[float, bool]:
    """
    Calculate airblast radius, considering crater formation.
    Returns (radius, qAirblast)
    """
    hkt = altitudeBurst / (energy_ktons ** (1.0 / 3.0))  # scaled burst altitude (m)
    radius = rkt * (energy_ktons ** (1.0 / 3.0)) / EARTH_RADIUS_KM  # radius of given damage effect

    qAirblast = False

    if qCrater:
        if radius < CraterRadiusFinal:
            radius = 0
        else:
            qAirblast = True
            if radius > 0.5 * math.pi:
                radius = CraterRadiusFinal
    else:
        # If scaled burst altitude is less than blast effect radius, compute based on slant range
        if hkt < rkt * 1000.0:
            qAirblast = True
            radius = math.sqrt(rkt ** 2 - (hkt / 1000.0) ** 2) * (energy_ktons ** (1.0 / 3.0)) / EARTH_RADIUS_KM
        else:
            radius = 0

    return radius, qAirblast


def find_airblast(energy_ktons, altitudeBurst, qCrater, CraterRadiusFinal):
    """
    Calculate airblast radii based on energy and crater type.

    Args:
        energy_ktons (float): Energy in kilotons.
        qCrater (bool): True if surface burst, else other.
    """
    if qCrater:
        values = [0.126, 0.155, 0.660, 1.651]  # kPa values for different damage levels
    else:
        values = [0.660, 1.651, 4.100]  # kPa values for different damage levels

    return [airblast_radius_crater(energy_ktons, rkt, altitudeBurst, qCrater, CraterRadiusFinal) for rkt in values]


def calc_energy(pdiameter, pdensity, vInput, velocity, theta, depth, distance):
    pi = math.pi
    R_earth=EARTH_RADIUS_KM * 1000  # in meters
    altitudeBurst=0

    # mass = density * volume, volume calculated assuming the projectile to be approximately spherical
    mass = ((pi * pdiameter ** 3) / 6) * pdensity
    energy0 = 0.5 * mass * (vInput * 1000) ** 2
    energy0_megatons = energy0 / (4.186 * 10 ** 15)  # joules to megatons conversion

    # Compute the recurrence interval for this energy impact (after Bland and Artemieva (2006) MAPS 41 (607-621).
    if mass < 3:
        rec_time = 10 ** (-4.568) * mass ** 0.480
    elif mass < 1.7E10:
        rec_time = 10 ** (-4.739) * mass ** 0.926
    elif mass < 3.3E12:
        rec_time = 10 ** (0.922) * mass ** 0.373
    elif mass < 8.4E14:
        rec_time = 10 ** (-0.086) * mass ** 0.454
    else:
        rec_time = 10 ** (-3.352) * mass ** 0.672

    # Use previous estimate at large sizes
    rec_time = max(rec_time, 110 * (energy0_megatons) ** 0.77)

    # If the impactor is less than a kilogram, the impactor burns up in the atmosphere
    if mass < 1:
        print_noimpact()
        return

    # Compute linear and angular momentum as a fraction of Earth's
    linmom = mass * (velocity * 1000)
    angmom = mass * (velocity * 1000) * math.cos(theta * pi / 180) * R_earth

    if vInput > (0.25 * 3 * 10 ** 5):  # relativistic effects
        beta = 1 / math.sqrt(1 - vInput ** 2 / (9 * 10 ** 10))
        energy0 *= beta
        linmom *= beta
        angmom *= beta

    lratio = angmom / EARTH_ANGULAR_MOMENTUM
    pratio = linmom / EARTH_LINEAR_MOMENTUM

    trot_change = (1.25 / pi) * (mass / EARTH_MASS) * math.cos(theta * pi / 180) / R_earth * velocity * (24. * 60. * 60.) ** 2

    # Compute energy of airburst, or energy after deceleration by atmosphere
    energy_atmosphere = 0.5 * mass * ((vInput * 1000) ** 2 - (velocity * 1000) ** 2)
    if altitudeBurst > 0:
        # Blast energy is airburst energy (kTons)
        energy_blast = energy_atmosphere / (4.186 * 10 ** 12)
        energy_surface = energy_atmosphere
    else:
        altitudeBurst = 0
        energy_surface = 0.5 * mass * (velocity * 1000) ** 2
        # Blast energy is larger of airburst and impact energy (kTons)
        if energy_atmosphere > energy_surface:
            energy_blast = energy_atmosphere / (4.186 * 10 ** 12)
        else:
            energy_blast = energy_surface / (4.186 * 10 ** 12)
    energy_megatons = energy_surface / (4.186 * 10 ** 15)  # joules to megatons conversion

    # Account for the decelerating effect of the water layer
    mwater = (pi * pdiameter ** 2 / 4) * (depth / math.sin(theta * pi / 180)) * 1000
    vseafloor = velocity * math.exp(-(3 * 1000 * 0.877 * depth) / (2 * pdensity * pdiameter * math.sin(theta * pi / 180)))
    energy_seafloor = 0.5 * mass * (vseafloor * 1000) ** 2

    # Compute the epicentral angle for use in several subsequent calculations.
    delta = (180 / pi) * (distance / R_earth)

    # Return results as a dictionary
    return {
        'mass': mass,
        'energy_joules': energy0,
        'energy0_megatons': energy0_megatons,
        'rec_time_years': rec_time,
        'linmom': linmom,
        'angmom': angmom,
        'lratio': lratio,
        'pratio': pratio,
        'trot_change': trot_change,
        'energy_atmosphere': energy_atmosphere,
        'energy_blast': energy_blast,
        'energy_surface': energy_surface,
        'energy_megatons': energy_megatons,
        'mwater': mwater,
        'vseafloor': vseafloor,
        'energy_seafloor': energy_seafloor,
        'delta': delta
    }


def find_crater(
    theta, depth, mass, target_density, pdiameter, velocity, vseafloor,
    dispersion, energy_seafloor
):
    # pi scaling diameter constants
    Cd = 1.6
    beta = 0.22

    anglefac = math.sin(theta * math.pi / 180) ** (1 / 3)

    wdiameter = None
    if depth != 0:
        # calculate crater in water using Cd = 1.88 and beta = 0.22
        wdiameter = 1.88 * (mass / target_density) ** (1 / 3) * \
            ((1.61 * G * pdiameter) / (velocity * 1000) ** 2) ** (-0.22)
        wdiameter *= anglefac
        target_density = 2700  # change target density for seafloor crater calculation

    # vseafloor == surface velocity if there is no water
    Dtr = Cd * (mass / target_density) ** (1 / 3) * \
        ((1.61 * G * pdiameter) / (vseafloor * 1000) ** 2) ** (-beta)
    Dtr *= anglefac

    if dispersion >= Dtr:
        # if crater field is formed, compute crater dimensions assuming
        # impact of largest fragment (with diameter = 1/2 initial diameter)
        Dtr /= 2

    depthtr = Dtr / 2.828

    if Dtr * 1.25 >= 3200:
        # complex crater will be formed, use equation from McKinnon and Schenk (1985)
        cdiameter = (1.17 * Dtr ** 1.13) / (3200 ** 0.13)
        depthfr = 37 * cdiameter ** 0.301
    else:
        # simple crater will be formed
        cdiameter = 1.25 * Dtr  # Diameter of final crater in m
        vbreccia = 0.032 * cdiameter ** 3  # Breccia lens volume in m^3
        rimHeightf = 0.07 * Dtr ** 4 / cdiameter ** 3  # Rim height of final crater in m
        brecciaThickness = 2.8 * vbreccia * ((depthtr + rimHeightf) / (depthtr * cdiameter ** 2))
        depthfr = depthtr + rimHeightf - brecciaThickness  # Final crater depth (in m)

    vCrater = (math.pi / 24) * (Dtr / 1000) ** 3
    vratio = vCrater / EARTH_VOLUME

    mratio = None
    mcratio = None
    vMelt = None

    if velocity >= 12:
        vMelt = MELT_COEFFICIENT * energy_seafloor * math.sin(theta * math.pi / 180)
        if vMelt > EARTH_VOLUME:
            vMelt = EARTH_VOLUME
        mratio = vMelt / EARTH_VOLUME
        mcratio = vMelt / vCrater

    CraterRadiusFinal = 0.5E-3 * cdiameter / EARTH_RADIUS_KM
    CraterRadiusTransient = 0.5E-3 * Dtr / EARTH_RADIUS_KM

    return {
        'CraterRadiusFinal': CraterRadiusFinal,
        'CraterRadiusTransient': CraterRadiusTransient,
        'Dtr': Dtr,
        'mratio': mratio,
        'wdiameter': wdiameter,
    }


def atmospheric_entry(pdensity, pdiameter, theta, vInput):
    # Yield strength of projectile in Pa
    yield_strength = 10 ** (2.107 + 0.0624 * math.sqrt(pdensity))

    # Velocity decrement factor
    av = 3 * RHO_SURFACE * DRAG_COEFFICIENT * SCALE_HEIGHT / (2 * pdensity * pdiameter * math.sin(theta * math.pi / 180))

    # Strength ratio
    rStrength = yield_strength / (RHO_SURFACE * (vInput * 1000) ** 2)

    iFactor = 5.437 * av * rStrength

    velocity = None
    altitudeBurst = None
    dispersion = 0

    if iFactor >= 1:  # projectile lands intact
        altitudeBurst = 0
        vTerminal = math.sqrt(2 * pdensity * pdiameter * G / (3 * RHO_SURFACE * DRAG_COEFFICIENT))
        vSurface = vInput * 1000 * math.exp(-av)

        if vTerminal > vSurface:
            velocity = vTerminal
        else:
            velocity = vSurface

    else:  # projectile does not land intact
        altitude1 = -SCALE_HEIGHT * math.log(rStrength)
        omega = 1.308 - 0.314 * iFactor - 1.303 * math.sqrt(1 - iFactor)
        altitudeBU = altitude1 - omega * SCALE_HEIGHT
        vBU = vInput * 1000 * math.exp(-av * math.exp(-altitudeBU / SCALE_HEIGHT))

        vFac = 0.75 * math.sqrt(DRAG_COEFFICIENT * RHO_SURFACE / pdensity) * math.exp(-altitudeBU / (2 * SCALE_HEIGHT))
        lDisper = pdiameter * math.sin(theta * math.pi / 180) * math.sqrt(pdensity / (DRAG_COEFFICIENT * RHO_SURFACE)) * math.exp(altitudeBU / (2 * SCALE_HEIGHT))

        alpha2 = math.sqrt(PANCAKE_FACTOR ** 2 - 1)
        altitudePen = 2 * SCALE_HEIGHT * math.log(1 + alpha2 * lDisper / (2 * SCALE_HEIGHT))
        altitudeBurst = altitudeBU - altitudePen

        if altitudeBurst > 0:  # impactor bursts in atmosphere
            expfac = (1 / 24) * alpha2 * (24 + 8 * alpha2 ** 2 + 6 * alpha2 * lDisper / SCALE_HEIGHT + 3 * alpha2 ** 3 * lDisper / SCALE_HEIGHT)
            velocity = vBU * math.exp(-expfac * vFac)
        else:
            altitudeScale = SCALE_HEIGHT / lDisper
            integral = (altitudeScale ** 3 / 3) * (
                3 * (4 + 1 / altitudeScale ** 2) * math.exp(altitudeBU / SCALE_HEIGHT)
                + 6 * math.exp(2 * altitudeBU / SCALE_HEIGHT)
                - 16 * math.exp(3 * altitudeBU / (2 * SCALE_HEIGHT))
                - 3 / altitudeScale ** 2
                - 2
            )
            velocity = vBU * math.exp(-vFac * integral)
            dispersion = pdiameter * math.sqrt(1 + 4 * altitudeScale ** 2 * (math.exp(altitudeBU / (2 * SCALE_HEIGHT)) - 1) ** 2)

    velocity /= 1000  # convert to km/s

    return {
        'residual_velocity': velocity,
        'altitudeBurst': altitudeBurst,
        'altitudeBU': altitudeBU,
        'dispersion': dispersion,
        'ifactor': iFactor
    }

def orbit_impact(pratio):
    if pratio >= 0.001:
        if pratio < 0.01:
            return "Noticeable"
        elif pratio < 0.1:
            return "Substantial"
        else:
            return "Total"
    else:
        return "Negligible"    


def describe_decibels(dec_level):
    if (dec_level == 0):
        return "The blast wave will not be heard."
    elif (dec_level <= 20): return "Barely Audible"
    elif (dec_level <= 50): return "Easily Heard"
    elif (dec_level <= 90): return "Loud as heavy traffic"
    elif (dec_level <= 120): return "May cause ear pain"
    else: return "Dangerously Loud"


def calculate_dispersion_ellipse(dispersion, theta, distance_km):
    if dispersion == 0 or distance_km == 0:
        return (0, 0)

    # Convert dispersion from meters to kilometers
    dispersion_km = dispersion / 1000.0

    # Calculate semi-major and semi-minor axes
    semi_major = dispersion_km * math.cos(theta * math.pi / 180) + distance_km * 0.01
    semi_minor = dispersion_km * math.sin(theta * math.pi / 180) + distance_km * 0.005

    return (semi_major, semi_minor)


def calculate_lost_energy(mass, entry_vkm, ending_vkm):
    return 0.5 * mass * (math.pow(entry_vkm * 1000, 2) - math.pow(ending_vkm * 1000, 2)) # in Joules


def air_blast(energy_blast, distance, altitudeBurst):
    vsound = 330          # speed of sound in m/s
    r_cross0 = 290        # radius at which relationship between overpressure and distance changes (for surface burst)
    op_cross = 75000      # overpressure at crossover

    energy_ktons = energy_blast

    # Arrival time is straight line distance divided by sound speed
    slantRange = math.sqrt(distance**2 + (altitudeBurst/1000)**2)  # for air burst, distance is slant range from explosion
    shock_arrival = (slantRange * 1000) / vsound  # distance in meters divided by velocity of sound in m/s

    # Scale distance to equivalent for a kiloton explosion
    sf = energy_ktons ** (1/3)
    d_scale = (distance * 1000) / sf

    # Scale burst altitude to equivalent for a kiloton explosion
    z_scale = altitudeBurst / sf
    r_cross = r_cross0 + 0.65 * z_scale
    r_mach = 550 * z_scale / (1.2 * (550 - z_scale))
    if z_scale >= 550:
      r_mach = 1e30

    if altitudeBurst > 0:
      d_smooth = z_scale**2 * 0.00328
      p_machT = ((r_cross * op_cross) / 4) * (1 / (r_mach + d_smooth)) * (1 + 3 * (r_cross / (r_mach + d_smooth)) ** 1.3)
      # p_0 = 3.1423e11 / z_scale**2.6
      # expFactor = -34.87 / z_scale**1.73
      # p_regT = p_0 * math.exp(expFactor * (r_mach - d_smooth))
      p_regT = 3.14e11 * ((r_mach - d_smooth) ** 2 + z_scale ** 2) ** (-1.3) + 1.8e7 * ((r_mach - d_smooth) ** 2 + z_scale ** 2) ** (-0.565)
    else:
      d_smooth = 0
      p_machT = 0

    if d_scale >= (r_mach + d_smooth):
      opressure = ((r_cross * op_cross) / 4) * (1 / d_scale) * (1 + 3 * (r_cross / d_scale) ** 1.3)
    elif d_scale <= (r_mach - d_smooth):
      # opressure = p_0 * math.exp(expFactor * d_scale)
      opressure = 3.14e11 * (d_scale ** 2 + z_scale ** 2) ** (-1.3) + 1.8e7 * (d_scale ** 2 + z_scale ** 2) ** (-0.565)
    else:
      opressure = p_regT - (d_scale - r_mach + d_smooth) * 0.5 * (p_regT - p_machT) / d_smooth

    # Wind velocity
    vmax = ((5 * opressure) / (7 * PO)) * (vsound / math.sqrt(1 + (6 * opressure) / (7 * PO)))

    ### sound intensity
    if (opressure > 0):
      dec_level = 20 * (math.log(opressure) / math.log(10));
    else:
      dec_level = 0;
 
    return dict(shock_arrival=shock_arrival, opressure=opressure, vmax=vmax, dec_level=dec_level, sound_description=describe_decibels(dec_level)    )


def find_thermal(energy_surface, energy_megatons):
  eta = 3e-3  # factor for scaling thermal energy
  T_star = 3000  # temperature of fireball
  Rf = 2e-6 * (energy_surface) ** (1/3)  # Rf is in km
  sigma = 5.67e-8  # Stephan-Boltzmann constant
  ignite_clothing = (energy_megatons) ** (1/6) * 1e6

  R_earth = EARTH_RADIUS_KM
  
  # Radius of fireball as a fraction of Earth radius
  RadiusFireball = Rf / R_earth

  # Radius of fireball visibility as a fraction of Earth radius
  RadiusVisibleFireball = math.acos(1 - RadiusFireball)

  # Radius at which clothing ignites
  r_upr = RadiusVisibleFireball * R_earth
  r_low = RadiusFireball * R_earth
  error = ignite_clothing
  count = 0
  r_guess = 0
  while abs(error) > 1e-3 * ignite_clothing and count < 10:
    count += 1
    r_guess = 0.5 * (r_low + r_upr)
    delta = r_guess / R_earth
    h = (1 - math.cos(delta)) * R_earth  # h is in km
    del_angle = math.acos(h / Rf)
    f = (2 / math.pi) * (del_angle - (h / Rf) * math.sin(del_angle))
    thermal_exposure = f * (eta * energy_surface) / (2 * math.pi * (r_guess * 1000) ** 2)
    error = thermal_exposure - ignite_clothing
    if error < 0.0:
      r_upr = r_guess
    else:
      r_low = r_guess

  RadiusClothingIgnition = r_guess / R_earth
  return dict(RadiusClothingIgnition=RadiusClothingIgnition, RadiusVisibleFireball=RadiusVisibleFireball, RadiusFireball=RadiusFireball)


def find_ejecta(Dtr, CraterRadiusTransient, CraterRadiusFinal):
    """
    Calculates the ejecta radii for various particle sizes given crater parameters.

    Args:
        Dtr (float): Diameter of the transient crater.
        CraterRadiusTransient (float): Radius of the transient crater.
        CraterRadiusFinal (float): Radius of the final crater.

    Returns:
        dict: A dictionary mapping particle size labels ('100m', '10m', '1m', '10cm', '1cm')
              to their corresponding ejecta radii as calculated by the `ejecta_radius` function.
    """
    return [(m, ejecta_radius(m, Dtr, CraterRadiusTransient, CraterRadiusFinal))
             for m in [0.01, 0.1, 1, 10, 100]]


def ejecta_radius(EjectaThickness, Dtr, CraterRadiusTransient, CraterRadiusFinal):
    third = 1.0 / 3.0
    radius = 1e-3 * (Dtr ** 4 / (112 * EjectaThickness)) ** third / EARTH_RADIUS_KM
    if radius > CraterRadiusTransient:
        qEjecta = 1
    else:
        radius = 0.0
    if radius > 0.5 * math.pi:
        radius = CraterRadiusFinal
    return radius


def find_seismic(energy_seafloor, CraterRadiusFinal):
    """
    Calculates the seismic effects of an impact event based on the energy at the seafloor and the final crater radius.

    The function estimates the earthquake magnitude generated by the impact, determines the radii at which various
    Modified Mercalli Intensity (MMI) levels are reached, and returns a list of tuples containing the MMI level and
    its corresponding radius.

    Parameters:
        energy_seafloor (float): The energy of the impact at the seafloor, typically in joules.
        CraterRadiusFinal (float): The final radius of the impact crater, in meters.

    Returns:
        List[Tuple[int, float]]: A list of tuples, each containing:
            - mercalli (int): The Modified Mercalli Intensity (MMI) level (3, 4, 7, 9, 12).
            - radius (float): The radius (in meters) from the impact center at which the given MMI level is experienced.
    """
    magnitude = 0.67 * (math.log(energy_seafloor) / math.log(10)) - 5.87
    qSeismic = 0
    RadiusMercalliIII = RadiusMercalliV = RadiusMercalliVII = RadiusMercalliIX = RadiusMercalliXII = 0

    if magnitude >= 3:
        RadiusMercalliIII = seismic_radius(magnitude, 3, CraterRadiusFinal)
        qSeismic = 1
    if magnitude >= 4:
        RadiusMercalliV = seismic_radius(magnitude, 4, CraterRadiusFinal)
    if magnitude >= 6:
        RadiusMercalliVII = seismic_radius(magnitude, 6, CraterRadiusFinal)
    if magnitude >= 7:
        RadiusMercalliIX = seismic_radius(magnitude, 7, CraterRadiusFinal)
    if magnitude >= 9:
        RadiusMercalliXII = seismic_radius(magnitude, 9, CraterRadiusFinal)

    return [(mercalli, radius) for mercalli, radius in [
        (3, RadiusMercalliIII),
        (4, RadiusMercalliV),
        (7, RadiusMercalliVII),
        (9, RadiusMercalliIX),
        (12, RadiusMercalliXII)
    ]]


def seismic_radius(mag, mag_eff, CraterRadiusFinal):
    radius1 = 42 * (mag - mag_eff) / EARTH_RADIUS_KM
    radius2 = 208 * (mag - mag_eff - 1.1644) / EARTH_RADIUS_KM
    radius3 = 10 ** ((mag - 6.399 - mag_eff) / 1.66)
    radius = max(radius1, radius2, radius3)
    if radius > 0.5 * math.pi:
        radius = CraterRadiusFinal
    return radius


def tsunami_radius(Rmax, Amax, Rexp, A, CraterRadiusFinal):
    radius = (Rmax / EARTH_RADIUS_KM) * (Amax / A) ** Rexp
    if radius > 0.5 * math.pi:
        radius = CraterRadiusFinal
    return radius


def find_tsunami(depth, wdiameter, CraterRadiusFinal):
    RimWaveExponent = 1.0
    MaxWaveRadius = 0.001 * wdiameter

    MaxWaveAmplitude = min(0.07 * wdiameter, depth)
    Radius1mTsunami = Radius10mTsunami = Radius100mTsunami = Radius1kmTsunami = 0

    if MaxWaveAmplitude > 1:
      Radius1mTsunami = tsunami_radius(MaxWaveRadius, MaxWaveAmplitude, RimWaveExponent, 1, CraterRadiusFinal)
    if MaxWaveAmplitude > 10:
      Radius10mTsunami = tsunami_radius(MaxWaveRadius, MaxWaveAmplitude, RimWaveExponent, 10, CraterRadiusFinal)
    if MaxWaveAmplitude > 100:
      Radius100mTsunami = tsunami_radius(MaxWaveRadius, MaxWaveAmplitude, RimWaveExponent, 100, CraterRadiusFinal)
    if MaxWaveAmplitude > 1000:
      Radius1kmTsunami = tsunami_radius(MaxWaveRadius, MaxWaveAmplitude, RimWaveExponent, 1000, CraterRadiusFinal)

    # Uncomment and adapt if collapse wave correction is needed
    # shallowness = pdiameter / depth
    # if shallowness < 0.5:
    #     CollapseWaveExponent = 3.0 * math.exp(-0.8 * shallowness)
    #     CollapseWaveRadius = 0.0025 * wdiameter
    #     MaxCollapseWaveAmplitude = 0.06 * min_val(wdiameter / 2.828, depth)
    #     CollapseWaveAmplitude = MaxCollapseWaveAmplitude * (CollapseWaveRadius / distance) ** CollapseWaveExponent
    #     WaveAmplitudeLowerLimit = min_val(CollapseWaveAmplitude, WaveAmplitudeLowerLimit)

    return [
      (1, Radius1mTsunami),
      (10, Radius10mTsunami),
      (100, Radius100mTsunami),
      (1000, Radius1kmTsunami)
    ]

def target_density(target_type):
    return {
        'water': 1000,
        'sedimentary': 2500,
        'crystalline': 2700}.get(target_type, 2500) 
