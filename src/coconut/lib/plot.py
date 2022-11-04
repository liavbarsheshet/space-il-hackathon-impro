from matplotlib import pyplot as plt
import numpy as np


# Creates custom plot and then returns figure to add to pdf
def createPlot(img, title, xLabel, yLabel, size=(10, 7)):
    # Creating a subplot
    figure, axes = plt.subplots(figsize=size)

    # Gives your plot a title
    plt.title(title)

    # Take the 2D Matrix of the chosen layer
    imgData = np.asarray(img)

    # Show the image on the plot
    plt.imshow(imgData)

    # Set names for the axis
    axes.set(xlabel=xLabel, ylabel=yLabel)

    return figure
