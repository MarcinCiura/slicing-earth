#!/usr/bin/python

import earth


def main():
  land = earth.ReadShapes('shapes/ne_10m_land')
  with open('great_circle_10m_a.txt', 'w') as log:
    for lat0, lat1, lon0, lon1 in [
        (4, 8, -108, -118), (23, 25, 78, 81), (51, 64, 45, 50),
        (49, 53, -3, -6), (42, 45, 153, 157), (76, 79, 98, 103),
        (0, 7, -151, -161)]:
      earth.EvaluateForMeshPoints(
          earth.GreatCircleLandFraction,
          lat0, lat1, lon0, lon1,
          0.5, land, log)
      print >>log

if __name__ == '__main__':
  main()
