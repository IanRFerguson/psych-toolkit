# ---------------------- IMPORTS
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps

matplotlib.use('Agg')

# ---------------------- MATCH TO LOCAL DIRECTORY HIERARCHY

here = os.getcwd()
faces = here + "/Faces/"                            # Directory with individual stimuli
output = here + "/Output/"                          # Directory to write to

# Create list of files in directory
single_im = [image for image in os.listdir(faces) if ".jpg" in image]

# Move to faces directory
os.chdir(faces)

# ---------------------- GENERATOR FUNCTION

def generateStims(left, right):

    border = (615,85,615,250)

    # Instantiate matplotlib object
    fig = plt.figure()

    # Left image
    ax1 = fig.add_subplot(1,1,1)
    face_l = Image.open(left)                        # Open and crop image from list
    face_l = ImageOps.crop(face_l, border)
    ax1.set_xticks([])                               # Format border (i.e., no tick marks!)
    ax1.set_yticks([])
    ax1.axis('off')
    plt.imshow(face_l)                               # Push image to matplotlib object

    # Right image
    ax2 = fig.add_subplot(1,2,2)
    face_r = Image.open(right)                       # Sim.
    face_r = ImageOps.crop(face_r, border)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.axis('off')
    plt.imshow(face_r)

    # Format and save to local directory
    fig.subplots_adjust(right=3)
    filename = "stim_{}_{}.png".format(left[7:14], right[7:14])
    fig.savefig(os.path.join(output, filename), bbox_inches="tight")
    plt.close()

# ---------------------- GENERATE STIMULI

# Loop through individual stimuli and generate pairwise stims

for left in single_im:
    for right in single_im:

        # Avoid duplicates!
        if left == right:
            continue

        generateStims(left, right)
