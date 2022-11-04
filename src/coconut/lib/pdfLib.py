from datetime import datetime

import matplotlib
from matplotlib.backends.backend_pdf import PdfPages as pdf
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects


class PDF:
    # Constructor
    def __init__(self, path):
        date = datetime.today().strftime("%b-%d-%Y")
        time = datetime.now().strftime("%H-%M-%S")
        self.path = f'{path}_{date}_{time}.pdf'
        self.pdf = None

    # Add plot figure to the pdf file
    def addFigure(self, figure):
        if not self.pdf:
            return
        self.pdf.savefig(figure)

    def open(self):
        if self.pdf:
            return
        self.pdf = pdf(self.path)

    def close(self):
        if not self.pdf:
            return
        self.pdf.close()
        self.pdf = None

    def write(self, fontSize, *text):
        if not self.pdf:
            return
        figure = plt.figure()

        textFig = figure.text(0.1, 0.85, '\n'.join(text), ha='left',
                              va='center', size=fontSize)
        textFig.set_path_effects([path_effects.Normal()])
        self.pdf.savefig(figure)

    def intro(self, *text):
        if not self.pdf:
            return
        figure = plt.figure()

        textFig = figure.text(0.5, 0.5, '\n'.join(text), ha='center',
                              va='center', size=20)
        textFig.set_path_effects([path_effects.Normal()])
        self.pdf.savefig(figure)
