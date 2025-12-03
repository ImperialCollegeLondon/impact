import math

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
    return f"{mantissa:.3f} x 10<sup>{exponent}</sup>"
