import click as ck
from pathlib import Path
import matplotlib.pyplot as plt

import database as db
import camera_input as inp
import model_wrapper as mw
import determine_matches as dm
import image_display as imd
import whispers_algorithm as whisp
import node as nd
import camera as cam

"""
Plan
----
Update the database
Identify faces in single image
Use whispers on folder of images
"""

@ck.command()
@ck.option("--dbpath", help="Path to database")
def update(dbpath):
	if database is not None:
		dbpath = Path(database)
		database.set_path(dbpath)

	img = cam.take_picture()
	
	boxes = mw.feed_mtcnn(img, threshold=probabilitythreshold) # ! Test for new threshold
	
	fingerprints = mw.compute_fingerprints(img, boxes)

@ck.command()
@ck.argument("filename", help="The path to the image that is to be analyzed")
@ck.option("-stdt", "--stdthreshold", type=ck.FLOAT, default=2.0)
@ck.option("-pt", "--probabilitythreshold", type=ck.FLOAT, default=0.8)
@ck.option("--dbpath", help="Path to database")
def find_faces(filename, stdthreshold, probabilitythreshold, dbpath):
	"""Command to find and identify faces in an image, label them with boxes and names from the database, and 
	display a final image with the aforementioned names and boxes. It labels unknown faces as "Unknown.""""

	if database is not None:
		dbpath = Path(database)
		database.set_path(dbpath)
	
	img = inp.import_image(Path(filename))
	
	boxes = mw.feed_mtcnn(img, threshold=probabilitythreshold) # ! Test for new threshold
	
	fingerprints = mw.compute_fingerprints(img, boxes)
	
	names = dm.determine_match(fingerprints, threshold=stdthreshold) # ! Test for new threshold
	
	imd.display_image(img, boxes, names)
	
@ck.command()
@ck.option("--dbpath", help="Path to database")
def init(dbpath):
	"""Initializes database at the path specified by --database (Defaults to ./database.pickle)
	"""
	if database is not None:
		dbpath = Path(database)
		database.set_path(dbpath)
	database.save({})

@ck.command()
@ck.argument("foldername")
@ck.option("-t", "--threshold", type=ck.FLOAT, default=1)
@ck.option("-m", "--maxiterations", type=ck.INT, default=200)
@ck.option("-w", "--weightededges", type=ck.BOOL, default=True)
def whispers(foldername, threshold, maxiterations, weightededges):
	"""Runs the whispers algorithm on a folder of images and graphs the final graph once it is complete"""
	
	graph = whisp.create_graph(foldername, threshold=threshold)
	
	adjacency_matrix = whisp.whispers(graph, threshold=threshold, max_iterations=maxiterations, weighted_edges=weightededges)
	
	# ! How do we use this function?
	fig, ax = nd.plot_graph(graph, adjacency_matrix)