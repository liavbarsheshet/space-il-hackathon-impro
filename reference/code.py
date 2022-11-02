import matplotlib
import scipy.io

import numpy as np
import glob
import pandas as pd

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

ImagesPath = ""


# Creates custom plot and then returns figure to add to pdf
def setPlot(img, title, xLabel, yLabel, size=(10, 7)):
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


# Initial Settings
matplotlib.use('Agg')  # Opens the plot not in runtime

# Fetch the Image files from folder path.
images = glob.glob(ImagesPath)

# Iterating through images src. img = image url, images = array of image urls
for img in images:
    # Fetch hs image data from file path
    curImg = scipy.io.loadmat(img)

    # Always the last key will be img name
    imgName = list(curImg.keys())[-1]

    # Converts the image pixels to 3D Array
    hsImg = np.asarray(curImg[imgName])

    # Gets the size of the 3D Image
    hsImgSize = hsImg.shape

    # Image Layers (how many layers would you like to save from image)
    hsLayers = [1, 20, 50, 60]

    # Creating a plot of the layers we chose
    # Iterating through all the layers [1,20,50,60]
    for layer in hsLayers:
        figure = setPlot(
            hsImg[:, :, layer],
            "Some Title",
            "X",
            "Y")

    # This part is for pre-processing data
    dataSet = []

    for x in range(0, hsImgSize[0]):
        for y in range(0, hsImgSize[1]):
            # Get the image at specific x,y while getting every data from z
            dataSet.append(hsImg[x, y, :])

    # Converts the dataSet list to numpy array
    dataSet = np.array(dataSet)

    # This is how many groups of clusters you want to differ
    segments = [2, 3, 4, 5]

    for cluster in segments:
        # Use KMeans algorithm to cluster the image.
        kMeans = KMeans(n_clusters=cluster)

        # Use the image data from data set.
        kMeans.fit(dataSet)

        # Creates 2D Matrix filled with zeros from given size
        pixels = np.zeros((hsImgSize[0], hsImgSize[1]))

        for x in range(0, hsImgSize[0]):
            for y in range(0, hsImgSize[1]):
                # Fill the pixels matrix with information about clustering
                # TODO: We need to check about the reshape parameters
                pixels[x, y] = kMeans.predict(hsImg[x, y, :].reshape(1, -1))

        figure = setPlot(
            pixels,  # Note here we send the pixels
            "Some Title",
            "X",
            "Y")


pdf = None


# PDF Handling Functions

# Opens a new or old pdf file
def pdfOpen(file):
    if pdf != None:
        return
    pdf = PdfPages(file)

# Close the current pdf file


def pdfClose():
    if (pdf == None):
        return
    pdf.close()
    pdf = None

# Saves figure to pdf


def addFigureToPdf(figure):
    pdf.savefig(figure)


# TODO: Please explore  matplotlib.backends.backend_pdf pdf creator lib
