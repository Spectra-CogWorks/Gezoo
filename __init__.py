import click as ck
from pathlib import Path

import database as db
import input as inp
import model_wrapper as mw
import determine_matches as dm
import image_display as imd
import whispers_algorithm as whisp

"""
Plan
----
Update the database
Identify faces in single image
Use whispers on folder of images

"""

@ck.command()
def update():
	

@ck.command()
@ck.argument("filename", help="The path to the image that is to be analyzed")
@ck.option("-stdt", "--stdthreshold", type=ck.FLOAT, default=2)
def find_faces(filename, stdthreshold):
	"""Command to find and identify faces in an image, label them with boxes and names from the database, and 
	display a final image with the aforementioned names and boxes. It labels unknown faces as "Unknown.""""
	
	img = inp.import_image(Path(filename))
	
	boxes = mw.feed_mtcnn(img) # ! Test for new threshold
	
	fingerprints = mw.compute_fingerprints(img, boxes)
	
	names = dm.determine_match(fingerprints) # ! Test for new threshold
	
	imd.display_image(img, boxes, names)
	
@ck.command()
@ck.option("--database", help="Path to database")
def init(database):
	"""Initializes database at the path specified by --database (Defaults to ./database.pickle)
	"""
	db_path = Path(database)
	database.set_path(db_path)
	database.save({})

@ck.command()
@ck.argument("foldername")
@ck.option("-t", "--threshold", type=ck.FLOAT, default=1)
def whispers(foldername, threshold):
	"""Runs the whispers algorithm on a folder of images and graphs the final graph once it is complete"""
	
	graph = whisp.create_graph()