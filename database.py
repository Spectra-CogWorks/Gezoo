import pickle
import numpy as np
from pathlib import Path
from copy import deepcopy
import model_wrapper as mw

class Database:
    def __init__(self, importVal=True, path="./database.pickle"):
        """Initialize a database, either fresh or imported
		
		Parameters
		----------
		import : boolean = True
			Choose whether there would should be a fresh dictionary or imported from a file
			
		path : str
			A path to the database path
		"""
        if importVal:
            self.database = pickle.load(open(path, "rb"))
        else:
            self.database = {}

    def save(self, datab, path="./database.pickle"):
        """Saves a database returned from default

		Parameters
		-------
		database: Dict{str : Profile]
			Single database instance containing profiles.
			
		path : str
			The path of the database
		"""
        datab = deepcopy(datab)
        pickle.dump(datab, open(path, "wb"))

    def load(self, path="./database.pickle"):
        """Loads a database

		Parameters
		-------
		path : str
			The path of the database
		
		Returns
		-------
		database : Dict{str : Profile}
		"""
        return pickle.load(open(path, "rb"))

    def add(self, name, fingerprint):
        """Adds a fingerprint to a specific database entry
		
		Parameters
		----------
		name : str
			The name key of the entry
			
		fingerprint : np.ndarray - shape(512,)
			The fingerprint being added to the database
		"""
        if name not in self.database:
            self.database[name] = [fingerprint]
        else:
            self.database[name].append(fingerprint)

    def add_multi(self, name, fingerprints):
        """Adds a fingerprint to a specific database entry
		
		Parameters
		----------
		name : str
			The name key of the entry
			
		fingerprints : List[np.ndarray - shape(512,)]
			The fingerprints being added to the database
		"""
        if name not in self.database:
            self.database[name] = fingerprints
        else:
            for fingerprint in fingerprints:
                self.database[name].append(fingerprint)

    def get_fingerprints(self, name):
        """The fingerprints are returned for a specific name
		
		Parameters
		----------
		name : str
			The key of the database
			
		Returns
		-------
		self.database[name] : List[np.ndarray - shape(512,)]
		"""
        return self.database[name]

    @classmethod
    def compute_fingerprint_from_image(cls, img):
        """Compute a fingerprint from an image
		
		Parameters
		----------
		img : np.ndarray
			An image
			
		Returns
		-------
		fingerprints : np.ndarray - shape(512,)
		"""
        return mw.compute_fingerprints(img, mw.feed_mtcnn(img))

