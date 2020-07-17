import pickle
import numpy as np
import database
from database import Profile

def add_fingerprint(fingerprints, names):
    """
    Checks whether the name for each fingerprint exists in the database.
    if not, it adds the name with a new Profile. 
    If it does, add a fingerprint to individual fingerprints.
    
    Parameters
    ----------
    fingerprints : np.ndarray with shape- (N,512)
        An array of fingerprints with N fingerprints
        
    names: List[String]
        List of names associated with the fingerprints above
        
    """
    #retrieves database
    db = database.default()
    #iterates through a range with num of fingerprints - 1
    for i in range(len(names)):
        #determines name and associated fingerprint
        name = names[i]
        fp = fingerprints[i,:]
        #checks if name is in database
        if name in db:
            #if so, adds fingerprint to list associated with name
            db[name].add(fp)
            print("name in db")
        #if not, creates a new profile and adds it to the database
        else:
            print("else")
            prof = Profile([fp])
            db[name] = prof
            print("completed!")
    database.save(db)