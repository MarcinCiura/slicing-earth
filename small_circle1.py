#!/usr/bin/python

import earth


def LargestCircleThroughOcean2(lat, lon, land):
  return earth.LargestCircleThroughOcean(
      lat, lon, land, r0=57, r1=53, rstep=0.01)

def main():
  land = earth.ReadShapes('shapes/ne_10m_land')
  with open('small_circle_10m.txt', 'w') as log:
    for lat0, lat1, lon0, lon1, lat_step in [
        (-61, -63, 110, 113, 0.1),
        (-64.3, -66.7, 135.0, 140.2, 0.1),
        (-9, -22, -140, -155, 0.5)]:
      earth.EvaluateForMeshPoints(
          LargestCircleThroughOcean2,
          lat0, lat1, lon0, lon1,
          lat_step, land, log)

if __name__ == '__main__':
  main()
