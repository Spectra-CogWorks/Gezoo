import click as ck
from pathlib import Path

"""
Plan
----
Update the database
Initialize the database
Identify faces in single image
Use whispers on folder of images
"""

@ck.command():
def update_database():
	pass

@ck.command()
def find_faces():
	pass
	
@ck.command()
def initialize_database():
	pass

@ck.command()
def run_whispers():
	pass