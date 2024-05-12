import numpy as np
import quaternion
import csv

class Camera:
  def __init__(self, xres, yres, fov):
    # fov in degrees
    # xres, yres in pixels
    self.xres = xres
    self.yres = yres
    self.xc = xres / 2
    self.yc = yres / 2
    self.fov = np.deg2rad(fov) # Horizontal FOV (radians)
    self.focal_length = xres / (2 * np.tan(self.fov / 2))

  def in_sensor(self, vec: np.ndarray) -> bool:
    # vec = 2D vector
    return vec[0] >= 0 and vec[0] <= self.xres \
      and vec[1] >= 0 and vec[1] <= self.yres


  def spatial_to_camera(self, vec: np.ndarray):
    """Project 3D spatial vector (relative to camera) to image plane coordinates

    vec = 3D vector relative to camera
    Note: define (X, 0, 0) <-> (xc, yc)
    """
    assert(vec[0] > 0)
    focal_factor = self.focal_length / vec[0]
    y = vec[1] * focal_factor
    z = vec[2] * focal_factor
    return np.array([self.xc - y, self.yc - z])

def rotate(q: np.quaternion, p):
  """Return coordinates of p wrt new coordinate system rotated by q about p
  Note: this is passive rotation, where the coordinate system is rotated by q w.r.t p
  p = 3D vector
  p' = q*p*q^-1 (* = quaternion multiplication)
  Returns 3D vector, i.e. coordinates of p w.r.t new coordinate system
  """
  res = q * np.quaternion(0, p[0], p[1], p[2]) * q.conjugate()
  return np.array([res.x, res.y, res.z])

class Star:
  """Class represents a star in the celestial sphere"""
  def __init__(self, id, spat_x, spat_y, spat_z, mag):
    self.id = id
    self.spatial = np.array([spat_x, spat_y, spat_z])
    self.mag = mag

  def __repr__(self):
    return f"id={self.id}, {self.spatial}, mag={self.mag}"

def parse_catalog(catalog_name: str) -> list:
  """Parse catalog into list of Stars

  Expected input format (per row): id, spat_x, spat_y, spat_z, mag
  """
  catalog = []
  with open(catalog_name, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
      catalog.append(Star(
          int(row[0]),
          float(row[1]), float(row[2]), float(row[3]),
          float(row[4])
      ))
  return catalog

def spherical_to_spatial(ra, de):
  """Return global 3D vector given RA, DE

  ra, de in degrees
  """
  ra = np.deg2rad(ra)
  de = np.deg2rad(de)
  return np.array([
      np.cos(ra) * np.cos(de),
      np.sin(ra) * np.cos(de),
      np.sin(de)
  ])

def get_quat(axis: np.ndarray, theta) -> np.quaternion:
  """Create a quaternion representing rotation of theta around axis

  axis = 3D vector
  theta in rad
  """
  f = np.sin(theta / 2)
  return np.quaternion(
    np.cos(theta/2),
    axis[0] * f,
    axis[1] * f,
    axis[2] * f
  )

def spherical_to_quat(att: np.ndarray):
  """Return quaternion that performs "improper" z-y'-x' Euler rotation (see LOST)

  ra, de, and roll in degrees
  """
  att = np.deg2rad(att)
  ra, de, roll = att

  a = get_quat(np.array([0, 0, 1]), ra)
  b = get_quat(np.array([0, 1, 0]), -de)
  c = get_quat(np.array([1, 0, 0]), -roll)
  res = (a * b * c).conjugate()
  assert np.abs(res.x**2 + res.y**2 + res.z**2 + res.w**2 - 1) <= 1e-4

  return res

def generate(catalog, cam: Camera, att: np.ndarray):
  """Return a list of centroid-star pairs that appear in the image plane when camera points at attitude

  att = 3D vector (ra, de, roll)
  Return format is a dict with following keys: att, centroids, stars
  """
  q = spherical_to_quat(att)
  centroids = []
  stars = []
  for star in catalog:
    rotated = rotate(q, star.spatial)
    if rotated[0] <= 0:
      continue
    centroid = cam.spatial_to_camera(rotated)
    if cam.in_sensor(centroid):
      centroids.append(centroid)
      stars.append(star)
  return {
      "att": att,
      "centroids": centroids,
      "stars": stars
  }