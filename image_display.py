import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

def display_image(imgarray, boxes, names):
    """
    Displays an image of people. These people have boxes surrounding them
    and their names depicted next to them.

    Parameters
    ----------
    imgarray : np.ndarray, shape=(H, W, C)
        The np.array that holds the image data. Where H is the height of the pic, W is the width, and C is the color channels.
    boxes : np.ndarray, shape=(B, 4)
        Np.ndarray where the corner coodinates are stored as xyxy and each row is a different box.
    names : List[String]
        Contains the names that correspond to each box.

    Returns
    -------
    None
    """

    fig, ax = plt.subplots() # pylint: disable=unused-variable
    ax.imshow(imgarray)

    for box, name in zip(boxes, names):
        ax.add_patch(Rectangle(box[:2], *(box[2:] - box[:2]), fill=None, lw=2, color="red"))
        plt.text(box[0], box[1], name, fontsize=28, color="green")
        
    plt.show(block=True)
    
