import numpy as np
import database

matches = []

def determine_match(fingerprints):
    """
	Parameter:
	-----------
	fingerprints: np.ndarray
		A shape-(N, 512) array of fingerprints (or descriptor vectors) taken from N images.
        	
	Returns:
	--------
	matches: list
		A list of the names whose fingerprints have the smallest cosine distance
        to each input/new fingerprint, i.e. are the best matches.
    """
    # loops over all N fingerprints in the input array
    for i in range(len(fingerprints)):
        name_dists = []
        mean_dists = []
        for name in database.keys():
            dists = []
            # each name contains multiple fingerprints
            for f in database[name]:
                # takes the cosine distances between input and database fingerprints for this name
                diff = cosine_distance(fingerprints[i], f)
                dists.append(diff)
            # computes mean distance and appends it to "name_dists"
            name_dists.append((name, np.mean(dists)))
            # appends mean distance for each name to "mean_dists"
            mean_dists.append(np.mean(dists))
        # appends the name with the lowest mean distance to list "matches" if it falls within 2 stds
        if (min(name_dists)[1] - np.mean(mean_dists)) <= 2 * np.std(mean_dists):
            matches.append(min(name_dists)[0])
        else:
            matches.append(None)

    return matches

def cosine_distance(d1, d2):
	"""
    Parameters:
    -----------
	d1: np.ndarray
		One of the two arrays you are finding the distance between.
    
    d2: np.ndarray
        The second of the two arrays you are finding the distance between.
        	
	Returns:
	--------
	float
        The cosine distance between the two arrays.
	"""
    return 1 - (np.matmul(d1, d2))/(np.linalg.norm(d1)*np.linalg.norm(d2))