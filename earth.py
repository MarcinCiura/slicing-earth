#!/usr/bin/python

import math
import sys

from cartopy import crs
from cartopy.io import shapereader
import numpy
from shapely import geometry
from shapely import geos


# The source projection for proj.transform_point()
# and proj.project_geometry(). This one serves as
# a no-op projection.
PLATE_CARREE = crs.PlateCarree()

# Small circles on a sphere are easy. I do not know
# how to specify their equivalent on an ellipsoid.
SPHERICAL_GLOBE = crs.Globe(ellipse='sphere')

EARTH_RADIUS_KM = 6370.997

def Project(lat, lon, land, klass=crs.Stereographic):
  proj = klass(
      central_longitude=lon,
      central_latitude=lat,
      globe=SPHERICAL_GLOBE)
  # Allow one metre of error. In fact, the error
  # is at most on the order of 1e-8 metres.
  assert math.hypot(*proj.transform_point(
      lon, lat, PLATE_CARREE)) <= 1.
  land_projected = [
      # buffer(0) fixes most problems with geometric
      # objects, such as self-crossing.
      proj.project_geometry(g, PLATE_CARREE).buffer(0)
      for g in land]
  return proj, land_projected

NUM_VERTICES = 3600

def Circle(lat, lon, radius_deg, proj):
  # (lon, clat) is a vertex of a polygon that
  # approximates the circle.
  # The correction makes the perimeter of the polygon
  # equal to the circumference of the circle.
  # For a 3600-gon, the correction factor is approximately
  # 7.6e-7.
  # The nonlinearity of the projection is negligible.
  shift = radius_deg * math.pi / (
      NUM_VERTICES * math.sin(math.pi / NUM_VERTICES))
  clat = lat + shift
  if clat > 90:
    clat = 180 - clat
    lon = lon + 180
  r = math.hypot(*proj.transform_point(
      lon, clat, PLATE_CARREE))
  return geometry.LinearRing(
      [(r * math.sin(t), r * math.cos(t))
      for t in numpy.linspace(
          0, 2 * math.pi, NUM_VERTICES, endpoint=False)])

def LengthOfIntersectionInKm(
    great_circle, land_projected):
  # The geometric objects in |land_projected|
  # only overlap on their boundaries.
  return sum(
      g.intersection(great_circle).length
      for g in land_projected) / great_circle.length * (
      2 * math.pi * EARTH_RADIUS_KM)

def GreatCircleLandFraction(lat, lon, land):
  proj, land_projected = Project(lat, lon, land)
  great_circle = Circle(lat, lon, 90, proj)
  try:
    return LengthOfIntersectionInKm(
        great_circle, land_projected)
  except geos.TopologicalError:
    # The exception is raised e.g. for (lat, lon) =
    # (6, -135) and land from 'ne_110m_land'.
    return -1.

def LargestCircleThroughOcean(
    lat, lon, land, r0=90, r1=0, rstep=0.1):

  def CircleIntersectsLand(lat, lon, r):
    circle = Circle(lat, lon, r, proj)
    return any(
        g.intersects(circle) for g in land_projected)

  proj, land_projected = Project(lat, lon, land)
  for r in numpy.linspace(
      r0, r1, abs(r1 - r0) / rstep + 1):
    try:
      if not CircleIntersectsLand(lat, lon, r):
        break
    except geos.TopologicalError:
      return -1.
  else:
    return r
  while rstep > 1e-10:
    rstep /= 2.
    rm = r + rstep
    circle = Circle(lat, lon, rm, proj)
    if not CircleIntersectsLand(lat, lon, rm):
      r = rm
  return r

def EvaluateForMeshPoints(
    fn, lat0, lat1, lon0, lon1, lat_step, land, log):
  for lat in numpy.linspace(
      lat0, lat1, abs(lat1 - lat0) / lat_step + 1):
    # Make the spacing of longitudes approximately
    # the same as the spacing of latitudes.
    endpoint = (abs(lon1 - lon0) != 360)
    num_lons = (
        abs(lon1 - lon0) / lat_step *
        math.cos(math.radians(lat)) + endpoint
        if abs(lat) != 90 else 1)
    for lon in numpy.linspace(
        lon0, lon1, num_lons, endpoint=endpoint):
      value = fn(lat, lon, land)
      print >>sys.stderr, lat, lon, value
      print >>log, lat, lon, value
      log.flush()

def ReadShapes(filename):
  shapes = list(shapereader.Reader(filename).geometries())
  # 'ne_110m_land' contains 127 MultiPolygons.
  # 'ne_10m_land' contains 1 MultiPolygon with 4063 Polygons.
  # Intersecting with multiple Polygons proves faster
  # than intersecting with one MultiPolygon.
  return shapes if len(shapes) > 1 else shapes[0]

def ReadShapes(filename):
  shapes = list(shapereader.Reader(filename).geometries())
  # 'ne_110m_land' contains 127 MultiPolygons.
  # 'ne_10m_land' contains 1 MultiPolygon with 4063
  # Polygons.
  # Intersecting with multiple Polygons proved faster
  # than intersecting with one MultiPolygon.
  return shapes if len(shapes) > 1 else shapes[0]

def main():
  # For this crude approximation, use land data dubbed
  # 'scale 1:110 million', with simplified coastline
  # and no smaller islands. Read a local copy.
  land = ReadShapes('shapes/ne_110m_land')
  with open('great_circle_110m.txt', 'w') as log:
    EvaluateForMeshPoints(
        GreatCircleLandFraction,
        0, 90, -180, +180,
        1, land, log)

if __name__ == '__main__':
  main()
