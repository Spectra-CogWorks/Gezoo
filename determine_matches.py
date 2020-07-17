import numpy as np
import database
from database import Profile

db = database.default()
matches = []

def determine_match(fingerprints, threshold=2):
    """
    Determines the best match out of the names in the database for each input fingerprint.
    
    Parameter:
    -----------
    fingerprints: np.ndarray
        A shape-(N, 512) array of fingerprints (or descriptor vectors) taken from N images.
        
    threshold : float
        The threshold value for standard deviations
        	
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
        print (db.keys())
        for name in db.keys():
            dists = []
            # each name contains multiple fingerprints
            for f in db[name]:
                # takes the cosine distances between input and database fingerprints for this name
                diff = cosine_distance(fingerprints[i], f)
                dists.append(diff)
                print ("dists : " + dists)
            # computes mean distance and appends it to "name_dists"
            name_dists.append((name, np.mean(dists)))
            print ("name_dists: " + name_dists)
            # appends mean distance for each name to "mean_dists"
            mean_dists.append(np.mean(dists))
            print ("mean_dists : " + mean_dists)
        # appends the name with the lowest mean distance to list "matches" if it falls within 2 stds
        if (min(mean_dists) - np.mean(mean_dists)) <= threshold * np.std(mean_dists):
            matches.append(name_dists[np.argmin(mean_dists)][0])
        else:
            matches.append(None)

    return matches

def cosine_distance(d1, d2):
    """
    Finds the cosine distance between two arrays.
    
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
