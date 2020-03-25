#!/usr/bin/python

import earth


def main():
  land = earth.ReadShapes('shapes/ne_110m_land')
  with open('small_circle_110m.txt', 'w') as log:
    earth.EvaluateForMeshPoints(
        earth.LargestCircleThroughOcean,
        -90, 90, -180, +180,
        1., land, log)

if __name__ == '__main__':
  main()
