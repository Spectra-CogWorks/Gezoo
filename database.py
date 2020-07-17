import pickle
import numpy as np
from pathlib import Path

_path = Path("./database.pickle")
_default = None

class Profile:
  def __init__(self, fingerprints):
    """Initialize a profile based on a list of fingerprints

    Parameters
    ----------
    fingerprints: List[np.ndarray]
      Accepts a list of size (512,) np.ndarrays to initialize the profile
    """
    self.fingerprints = fingerprints

  def add(self, fingerprint):
    """Add a new fingeprint to the database

    Parameters
    ----------
    fingerprint: np.ndarray
      Accepts a size (512,) np.ndarray to add to the profile
    """
    self.fingerprints.append(fingerprint)

  @property
  def mean(self):
    """Returns the mean fingerprint

    Returns
    -------
    fingerprint: np.ndarray
      A size (512,) np.ndarray representing the mean fingerprint
    """
    return np.mean(self.fingerprints, axis=0)

  @property
  def stddev(self):
    """Returns the standard deviation fingerprint

    Returns
    -------
    fingerprint: np.ndarray
      A size (512,) np.ndarray representing the standard deviation fingerprint
    """
    return np.std(self.fingerprints, axis=0)

def set_path(path):
  """Sets path to be used to load the database.

  Parameters
  ----------
  path: Path
    Path to load database from.
  """
  global _path
  _path = path  

def default():
  """Returns the database of profiles.

  Returns
  -------
  database: Dict[str, Profile]
    Single database instance containing profiles.
  """
  global _default
  global _path

  if _default:
    return _default
  else:
    _default = pickle.load(open(_path, "rb"))

    for name, fingerprints in enumerate(_default):
      _default[name] = Profile(fingerprints)

    return _default

def save(database):
  """Saves a database returned from default

  Parameters
  -------
  database: Dict[str, Profile]
    Single database instance containing profiles.
  """
  global _default
  global _path

  for name, profile in enumerate(database):
    database[name] = profile.fingerprints

  _default = database

  pickle.dump(_default, open(_path, "wb"))
