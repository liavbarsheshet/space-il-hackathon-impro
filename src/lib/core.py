import matplotlib
import scipy.io
import numpy as np
import pandas as pd
from datetime import datetime

import lib.pdfLib as pdf
import lib.plot as plot
import sys

# TODO: Need to change the algorithms
from sklearn.cluster import KMeans


# TODO: Change The Algo
def clusterData(img, options):
    # Custom Segments
    segments = options['segments'] if 'segments' in options and isinstance(
        options['segments'], list) else [3, 5, 7]

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
            pixels, f"{cluster} Segmentation", 'Width', 'Height')

        img['pdf'].addFigure(figure)


def compressBands(img):
    blob = img['blob']
    width = img['size'][0]
    height = img['size'][1]
    depth = img['size'][2]
    components = 15

    # Initialize Dataset
    zSum = []

    # # Process Data Set
    for z in range(0, depth):
        sum = 0
        for x in range(0, width):
            for y in range(0, height):
                sum = sum+blob[x, y, z]
        zSum.append({
            'sum': sum,
            'z': z
        })

        zSum.sort(key=lambda val: val['sum'])

    length = len(zSum)
    skips = length//components

    bands = []

    for i in range(0, length, skips):
        bands.append(zSum[i]['z'])

    bands.sort()

    newBlob = np.zeros((width, height, len(bands)))

    for x in range(0, width):
        for y in range(0, height):
            for z in range(len(bands)):
                newBlob[x, y, z] = blob[x, y, bands[z]]

    img['blob'] = np.asarray(newBlob)

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
            img['blob'][:, :, layer], f"Sample {layer}nm", 'Width', 'Height')
        img['pdf'].addFigure(figure)


def processImages(images, options):
    startTime = datetime.now().timestamp()
    if not isinstance(images, list):
        raise Exception('Invalid images')

    pdfPage = pdf.PDF(f"./result/coconut")
    pdfPage.open()
    pdfPage.intro('COCONUT RESULT')

    for imgSrc in images:
        img = {}

        # Fetch hs image data from file path
        img['data'] = scipy.io.loadmat(imgSrc)

        # Gets File Full Name
        img['full-name'] = imgSrc.split('/')[-1]

        # Get image name
        img['name'] = list(img['data'].keys())[-1]

        pdfPage.intro(img['name'])

        # Converts the image pixels to 3D Array
        img['blob'] = np.asarray((img['data'][img['name']]))

        # Gets image size
        img['size'] = img['blob'].shape

        img['pdf'] = pdfPage

        # Get layers if exists in options o.w set default sample layers
        layers = options['layers'] if 'layers' in options else [1, 20, 50, 60]

        # Opens pdf output

        print('Processing Sample Layers')
        # Sampling Bands
        sampleLayers(img, layers)
        print('Processing Sample Layers : DONE!')

        print('Compressing Data')
        # Compress Bands
        compressBands(img)

        # Creates Data Set
        processData(img)
        print('Compressing Data : DONE!')

        print('Image Clustering')
        # Image Clustering
        clusterData(img, options)
        print('Image Clustering DONE!')

        print('')

        timeDiffer = datetime.now().timestamp() - startTime

        print(f'DONE: Took {timeDiffer}s')

    pdfPage.close()
