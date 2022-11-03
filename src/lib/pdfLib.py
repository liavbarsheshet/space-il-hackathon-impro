from datetime import datetime

import matplotlib
from matplotlib.backends.backend_pdf import PdfPages as pdf


class PDF:
    # Constructor
    def __init__(self, path):
        date = datetime.today().strftime("%b-%d-%Y")
        time = datetime.now().strftime("%H-%M-%S")
        self.path = f'{path}_{date}_{time}.pdf'
        self.pdf = None

    # Add plot figure to the pdf file
    def addFigure(self, figure):
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
