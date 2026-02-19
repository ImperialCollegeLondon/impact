import math
from sigfig import round

def format_duration(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes} minutes, {seconds} seconds"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours} hours, {minutes} minutes, {seconds} seconds"

def format_scientific(value):
    if value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value))))
    mantissa = value / (10 ** exponent)
    return f"{round(mantissa, 2)} x 10<sup>{exponent}</sup>"


def format_sig_figs(value, sigfigs):
    return round(value, sigfigs)
    """Format a number to the given significant figures."""
    if value == 0:
      return "0"
    from math import log10, floor
    digits = -int(floor(log10(abs(value)))) + (sigfigs+1)
    fmt = "{:." + str(max(0, digits)) + "g}"
    return fmt.format(value)


def format_distance(distance_meters, sigfigs):
    """
    Format distance_meters into appropriate units and significant figures.
    Returns a tuple: (value1, unit1, value2, unit2)
    """
    # Convert to cm, microns or km
    if distance_meters < 0.001:
      value1 = format_sig_figs(distance_meters * 1_000_000, sigfigs)
      unit1 = "microns"
      value2 = format_sig_figs(distance_meters * 39400, sigfigs)  # meters to thousandths of an inch
      unit2 = "thousandths of an inch"
    elif distance_meters < 0.01:
      value1 = format_sig_figs(distance_meters * 1000, sigfigs)
      unit1 = "mm"
      value2 = format_sig_figs(distance_meters * 394, sigfigs)  # meters to tenths of an inch
      unit2 = "tenths of an inch"
    elif distance_meters < 1:
      value1 = format_sig_figs(distance_meters * 100, sigfigs)
      unit1 = "cm"
      value2 = format_sig_figs(distance_meters * 39.37, sigfigs)  # meters to inches
      unit2 = "inches"
    elif distance_meters > 1000:
      value1 = format_sig_figs(distance_meters * 0.001, sigfigs)
      unit1 = "km"
      value2 = format_sig_figs(distance_meters * 0.000621, sigfigs)  # meters to miles
      unit2 = "miles"
    else:
        value1 = format_sig_figs(distance_meters, sigfigs)
        unit1 = "meters"
        value2 = format_sig_figs(distance_meters * 3.28, sigfigs)  # meters to feet
        unit2 = "feet"

    return value1, unit1, value2, unit2