#!/usr/bin/python

from cartopy import feature
from matplotlib import pyplot

import earth


def main():
  lat, lon, radius = 50, 20, 90
  lands = earth.ReadShapes('shapes/ne_110m_land')
  proj, lands_projected = earth.Project(lat, lon, lands)
  pyplot.figure(figsize=(6, 6))
  ax = pyplot.axes(projection=proj)
  lands_feature = feature.ShapelyFeature(
      lands_projected,
      proj,
      edgecolor='none',
      facecolor='black')
  ax.add_feature(lands_feature)
  ax.gridlines(
      edgecolor='#bbbbbb',
      linestyle='-',
      linewidth=1)
  pyplot.savefig('Centre-in-Krakow.png', bbox_inches='tight')

if __name__ == '__main__':
  main()
