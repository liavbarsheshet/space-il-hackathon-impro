import matplotlib
import scipy.io
import numpy as np
import pandas as pd

import lib.pdfLib as pdf
import lib.plot as plot

# TODO: Need to change the algorithms
from sklearn.cluster import KMeans


# TODO: Change The Algo
def clusterData(img, options):
    # Custom Segments
    segments = options['segments'] if 'segments' in options and isinstance(
        options['segments'], list) else [2, 3, 4, 5]

    # DataSet
    dataSet = img['data-set']
    blob = img['blob']

    # Image Dimension
    width = img['size'][0]
    height = img['size'][1]

    for cluster in segments:

        # Use KMeans algorithm to cluster the image.
        kMeans = KMeans(n_clusters=cluster)

        # Use the image data from data set.
        kMeans.fit(dataSet)

        # Creates 2D Matrix filled with zeros from given size
        pixels = np.zeros((width, height))

        for x in range(0, width):
            for y in range(0, height):
                pixels[x, y] = kMeans.predict(blob[x, y, :].reshape(1, -1))

        # Creates Plot
        figure = plot.createPlot(
            pixels, f"Output Cluster of {cluster} from {img['name']}", 'Width', 'Height')

        img['pdf'].addFigure(figure)

# Function that will process DataSet


def processData(img):
    blob = img['blob']
    width = img['size'][0]
    height = img['size'][1]

    # Initialize Dataset
    dataSet = []

    # Process Data Set
    for x in range(0, width):
        for y in range(0, height):
            dataSet.append(blob[x, y, :])

    img['data-set'] = np.array(dataSet)


def sampleLayers(img, layers):
    if not isinstance(layers, list):
        raise Exception('Invalid layers sample')
    for layer in layers:
        if not isinstance(layer, int):
            raise Exception('Invalid layers sample')
        figure = plot.createPlot(
            img['blob'][:, :, layer], f"Band Sample from {img['name']}\nBand Layer: {layer}", 'Width', 'Height')
        img['pdf'].addFigure(figure)


def processImages(images, options):
    if not isinstance(images, list):
        raise Exception('Invalid images')
    for imgSrc in images:
        img = {}

        # Fetch hs image data from file path
        img['data'] = scipy.io.loadmat(imgSrc)

        # Gets File Full Name
        img['full-name'] = imgSrc.split('/')[-1]

        # Get image name
        img['name'] = (img['full-name'].lower()).split('.')[0]

        # Converts the image pixels to 3D Array
        img['blob'] = np.asarray((img['data'][img['name']]))

        # Gets image size
        img['size'] = img['blob'].shape

        img['dest'] = options['dest'] if 'dest' in options else './result'

        img['pdf'] = pdf.PDF(f"{img['dest']}/{img['name']}")

        # Get layers if exists in options o.w set default sample layers
        layers = options['layers'] if 'layers' in options else [1, 20, 50, 60]

        # Opens pdf output
        img['pdf'].open()

        # Sampling Bands
        sampleLayers(img, layers)

        # Creates Data Set
        processData(img)

        # Image Clustering
        clusterData(img, options)

        img['pdf'].close()
    pass
