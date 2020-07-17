"""
This module contains the implementation of the whispers algorithm and its associated functions
"""

import numpy as np
from pathlib import Path
import random

import node as nd
import model_wrapper as mw
from determine_matches import cosine_distance
import input
from input import import_folder

def create_graph(folder_path, threshold):
    """
    Creates a list of nodes, imports images, and fills the nodes with their respective information
    
    Parameters
    ----------
    folder_path : str
        The path to a folder containing solely images
        
    threshold : 
        the maximum distance that determines the edges
    
    Returns
    -------
    graph : List[Node]
        This is a list of the initialized and filled nodes
    """
    list_of_nodes = []
    
    imglist = import_folder(folder_path)
    node_num = 0
    
    for image in imglist:
        fingerprints = mw.compute_fingerprints(image, mw.feed_mtcnn(image))

        for face in fingerprints:
            new_node = Node(node_num, [], face, image=image)
            list_of_node.append(new_node)
            node_num += 1

    for node1 in list_of_nodes:
        for node2 in list_of_nodes:
            if node1 is not node2:
                if cosine_distances(node1.descriptor, node2.descriptor) < threshold:
                    node1.neighbors.append(node2.ID)
                    
    return list_of_nodes        


def whispers(graph, threshold, max_iterations, weighted_edges):
    """
    Using the graph, creates an adjacency matrix which details a relationship between the nodes, aka "edges". 

    Parameters
    ----------
    graph : List[Node]
 
        This is a list of all the nodes
        
    threshold : float
        The threshold distance to decide whether two nodes should have an edge
    
    max_iterations : 
        The maximum number of iterations the algorithm should go through before stopping
        
    weighted_edges : bool=True
        The option of using weighted edges in the function. Default value is True
    
    Returns
    -------
    None
    """
    # TODO Create a windowed average for the convergence check
    # Create the adjacency matrix
    adjacency_matrix = np.zeros((len(graph), len(graph)))
    
    # Populate the adjacency matrix
    # If weighted edges is enabled, the matrix will contain values in [0, infinity) instead of [0, 1]
    for node in graph:
        for neighbor in node.neighbors:
            distance = cosine_distance(node.descriptor, graph[neighbor].descriptor)
            
            if distance < threshold:
                adjacency_matrix[node.ID, neighbor] = 1 / (distance ** 2) + 1 if weighted_edges else 1
                adjacency_matrix[neighbor, node.ID] = 1 / (distance ** 2) + 1 if weighted_edges else 1

    # Selecting random node
    # Initializing label counts to be able to detect when convergence occurs (i.e. the number of labels stays the same)
    num_labels_count = len(graph)
    past_labels = num_labels_count

    # Randomly selecting a node and then updating its label by finding the neighbor with the highest frequency
    for i in max_iterations: # pylint: disable=unused-variable
        node = random.choice(graph)
        
        if len(node.neighbors) != 0:
            
            # Checking all the neighbors for which has the highest frequency
            frequencies = [] # list of tuples (neighbor_index, freq)
            for neighbor_index, neighbor in enumerate(node.neighbors):
                frequencies.append((neighbor_index, adjacency_matrix[node.ID, neighbor]))
            
            # Convert list to np.ndarray to allow slicing
            frequencies = np.array(frequencies)
            
            # Slice frequencies to find the first max frequency
            max_freq = np.amax(frequencies[:, 1])
            max_dupl_indices = [] # list of ints
            
            # loops through all the frequencies and determines the indices of the max_freq
            for neighbor_index, freq in frequencies:
                if freq == max_freq:
                    # max_dupl_indices contains the indices of the all the neighbors that
                    # have the max value
                    max_dupl_indices.append(neighbor_index)
                    
            if len(max_dupl_indices) > 1:
                max_freq_index = random.choice(max_dupl_indices)
            else:
                max_freq_index = max_dupl_indices[0]
            
            # Updating the label
            new_label = graph[node.neighbors[max_freq_index]].label
            
            # Checking that the number of labels is changing to subtract from the number of labels
            if new_label != node.label:
                num_labels_count -= 1
            
            node.label = graph[node.neighbors[max_freq_index]].label
            
            # Checks that the number of labels isn't the same before
            if num_labels_count == past_labels:
                break
                
            past_labels = num_labels_count
