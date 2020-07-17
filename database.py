import pickle
from pathlib import Path

_path = Path("./database.pickle")
_default = None

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
    return _default
  
    