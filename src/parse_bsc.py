"""
Code to parse and filter YBSC
Example usage:

```
from parse_bsc import *

write_filtered_catalog("bsc.tsv", "filter-catalog.csv", 6, 0.05)
```
"""

import csv
import numpy as np

from sky_helper import *

def angle(u, v):
  """Return angle (in radians) between u and v

  u dot v = |u||v|cos(theta)
  cos(theta) = (u dot v) / |u||v|
  """
  prod = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
  if prod >= 1:
    return 0
  if prod <= -1:
    return np.pi
  return np.arccos(prod)

class CatalogStar:
  def __init__(self, ra:float, de:float, mag:float, id:int):
    # ra, de in degrees
    self.spatial = spherical_to_spatial(ra, de)

    self.mag = mag
    self.id = id

  def __repr__(self):
    return f"id={self.id}, {self.spatial}, mag={self.mag}"

def parse_bsc(bsc_fname: str):
  """Parse BSC into a list of CatalogStars"""
  catalog = []
  with open(bsc_fname) as f:
    f = csv.reader(f, delimiter="|")
    for line in f:
      ra=float(line[0])
      de=float(line[1])
      catalog.append(CatalogStar(
          ra=ra, de=de,
          mag=float(line[-1]), id=int(line[2])
      ))

  num_stars = len(catalog)
  print(f"Initial catalog size = {num_stars}")
  return catalog

def filter_catalog(catalog, max_mag: float, min_sep: float):
  """Filter catalog by removing double stars, dim stars

  min_sep in degrees, max_mag in Mv
  """
  res = []
  min_sep = np.deg2rad(min_sep)
  for star in catalog:
    if star.mag <= max_mag:
      res.append(star)

  num_stars = len(res)
  print(f"passed mag filter = {num_stars}")

  double_stars = set()
  for i in range(num_stars):
    for j in range(i+1, num_stars):
      if angle(res[i].spatial, res[j].spatial) < min_sep:
        double_stars.add(i)
        double_stars.add(j)

  for i in reversed(range(num_stars)):
    if i in double_stars:
      del res[i]

  print(f"passed double stars = {len(res)}")
  return res

def write_filtered_catalog(bsc_fname, filtered_fname, max_mag: float, min_sep: float):
  catalog = parse_bsc(bsc_fname)
  with open(filtered_fname, "w+") as f:
    filtered_catalog = filter_catalog(catalog, max_mag, min_sep)
    writer = csv.writer(f)
    writer.writerow(["ID", "spat_x", "spat_y", "spat_z", "mag"])
    for star in filtered_catalog:
      writer.writerow([star.id] + [vi for vi in star.spatial] + [star.mag])


