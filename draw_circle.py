#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import sys

from cartopy import crs
from cartopy import feature
from matplotlib import pyplot
import numpy

import earth


def FormatDegrees(x, quarter):
  if x > 0:
    direction = quarter[0]
  else:
    x = -x
    direction = quarter[1]
  deg = int(x)
  sec = int(3600 * (x - deg) + 0.5)
  mnt = sec // 60
  sec = sec % 60 
  return u'%d\u00b0%02d\u2032%02d\u2033%s'% (deg, mnt, sec, direction)

def MakeCentreTitle(lat, lon):
  return u'Map centre at %s %s' % (
      FormatDegrees(lat, 'NS'),
      FormatDegrees(lon, 'EW'))

def MakeTitle(lat, lon, radius, intersection):
  centre = MakeCentreTitle(lat, lon)
  if radius == 90:
    return u'%s\n%.f km of land' % (centre, intersection)
  else:
    r = math.sin(math.radians(radius)) * earth.EARTH_RADIUS_KM
    return u'%s\nRadius %.f km' % (centre, r)

def main():
  if len(sys.argv) < 5:
    sys.exit('Required args: lat lon radius filename')
  lat, lon, radius = [float(x) for x in sys.argv[1:4]]
  filename = sys.argv[4]
  land = earth.ReadShapes('shapes/ne_10m_land')
  klass = crs.AzimuthalEquidistant if radius == 90 else crs.Orthographic
  proj, land_projected = earth.Project(lat, lon, land, klass)
  circle = earth.Circle(lat, lon, radius, proj)

  pyplot.figure(figsize=(6, 6))
  ax = pyplot.axes(projection=proj)
  land_feature = feature.ShapelyFeature(
      land_projected,
      proj,
      edgecolor='none',
      facecolor='black')
  circle_feature = feature.ShapelyFeature(
      [circle],
      proj,
      linewidth=1,
      edgecolor='blue',
      facecolor='none')
  intersection_feature = feature.ShapelyFeature(
      [g.intersection(circle) for g in land_projected],
      proj,
      linewidth=1,
      edgecolor='yellow',
      facecolor='none')
  ax.add_feature(land_feature)
  ax.add_feature(circle_feature)
  ax.add_feature(intersection_feature)
  ax.gridlines(
      edgecolor='#bbbbbb',
      linestyle='-',
      linewidth=0.5)
  pyplot.title(MakeTitle(
      lat, lon, radius,
      earth.LengthOfIntersectionInKm(circle, land_projected)))
  pyplot.savefig(filename, bbox_inches='tight')

if __name__ == '__main__':
  main()
