#!/usr/bin/python

import earth


def main():
  land = earth.ReadShapes('shapes/ne_10m_land')
  with open('great_circle_10m_b.txt', 'w') as log:
    for lat0, lat1, lon0, lon1 in [
        (3.7, 6.2, -112.5, -116.5), (23.5, 24.5, 78.5, 80.5),
        (56.5, 59, 46, 49), (50.5, 51.5, -3.5, -6.5),
        (43, 44.5, 153.5, 155.5), (76.5, 78.5, 98, 101),
        (3.2, 5.2, -153, -156)]:
      earth.EvaluateForMeshPoints(
          earth.GreatCircleLandFraction,
          lat0, lat1, lon0, lon1,
          0.1, land, log)
      print >>log

if __name__ == '__main__':
  main()
