from models import model
import uuid 
import math

EARTH_RADIUS = 6371

def haversine_dist(a, b):
    if a.type == b.type:
        raise TypeError()
    p_lat = math.radians(float(str(a.lat)))
    p_lng = math.radians(float(str(a.lng)))
    d_lat = math.radians(float(str(b.lat)))
    d_lng = math.radians(float(str(b.lng)))

    for value in [p_lat, p_lng, d_lat, d_lng]:
        if value == "":
            raise ValueError()
        if math.isnan(value):
            raise TypeError()
    for value in [p_lat, d_lat]:
        if float(value) > math.pi/2 or float(value) < -math.pi/2:
            raise ValueError()
    for value in [p_lng, d_lng]:
        if float(value) > math.pi or float(value) < -math.pi:
            raise ValueError()
    delta_lat = p_lat - d_lat
    delta_lng = p_lng - d_lng

    h = math.sin(delta_lat/2) ** 2 + math.cos(p_lat) * math.cos(d_lat) * math.sin(delta_lng/2) ** 2

    radians = 2 * math.atan2(math.sqrt(h), math.sqrt(1-h))

    return radians * EARTH_RADIUS
