#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import sys

from cartopy import crs
from cartopy import feature
from matplotlib import pyplot
import numpy

import earth


def main():
  lat, lon, radius = -66.10165712, 136.51515176, 55.957758952975269
  filename = 'Torres-Strait.png'
  land = earth.ReadShapes('shapes/ne_10m_land')
  klass = crs.AzimuthalEquidistant
  proj, land_projected = earth.Project(lat, lon, land, klass)
  circle = earth.Circle(lat, lon, radius, proj)

  pyplot.figure(figsize=(6, 6))
  ax = pyplot.axes(projection=proj)
  ax.set_extent([123, 153, -32, 0])
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
  pyplot.savefig(filename, bbox_inches='tight', pad_inches=0.2)

if __name__ == '__main__':
  main()
