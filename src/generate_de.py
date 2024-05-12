# Example script to generate clean data corresponding to given DE split

import sys
import json

from sky_helper import *

def main():

  start = int(sys.argv[1])
  end = int(sys.argv[2])

  print("Beginning data generation")
  print(f"DE split beginning [{start}, {end})")

  xres = 500
  yres = 500
  fov = 12
  cam = Camera(xres, yres, fov)

  catalog = parse_catalog("filter-catalog.csv") # filter catalog: max mag 6.0 Mv
  print("filtered catalog length", len(catalog))

  # Generate dataset
  dataset = []

  for de in range(start, end):
    for ra in range(0, 360):
      print(f"de {de}, ra {ra}")
      for roll in range(0, 360, 5):
        res = generate(catalog, cam, np.array([ra, de, roll]))
        dataset.append(res)

  ser_dataset = [{
      "att": cd["att"].tolist(),
      "centroids": [cc.tolist() for cc in cd["centroids"]],
      "stars": [star.id for star in cd["stars"]],
      "mags": [star.mag for star in cd["stars"]]
  } for cd in dataset]

  with open(f"clean-de-{start}-{end}.json", "w") as f:
    json.dump(ser_dataset, f)

if __name__=="__main__":
  main()


