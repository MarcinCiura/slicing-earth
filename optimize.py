#!/usr/bin/python

import sys

import numpy
from scipy import optimize

import earth


def LandFraction(latlon, land):
  result = earth.GreatCircleLandFraction(
      latlon[0], latlon[1], land)
  print >>sys.stderr, latlon, result
  return result

def NegativeLandFraction(latlon, land):
  return -LandFraction(latlon, land)

def NegativeCircleRadius(latlon, land):
  result = earth.LargestCircleThroughOcean(
      latlon[0], latlon[1], land,
      r0=57, r1=53, rstep=0.01)
  print >>sys.stderr, latlon, result
  return -result

METHOD = 'Nelder-Mead'

def main():
  land = earth.ReadShapes('shapes/ne_10m_land')
  for x0 in [
      (5.2, -114.45), (24.1, 79.17), (57.5, 46.75),
      (50.7, -4.76), (44.1, 154.79), (77.4, 100.5)]:
    print optimize.minimize(
        LandFraction, x0=x0, args=(land,), method=METHOD)
  print optimize.minimize(
      NegativeLandFraction, x0=(3.4, -154.14),
      args=(land,), method=METHOD)
  for x0 in [(-65.9, 136.73), (-15.0, -149.64)]:
    print optimize.minimize(
        NegativeCircleRadius, x0=x0, args=(land,), method=METHOD)

if __name__ == '__main__':
  main()
