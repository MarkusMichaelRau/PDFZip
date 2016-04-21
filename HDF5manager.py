import pandas as pd


pdfkey = 'pdf'


def readUncompressedPDF(fname, chunksize):
    return pd.read_hdf(fname, pdfkey, chunksize=chunksize)


def writeUncompressedPDF(fout, pdDataFrame):
    pdDataFrame.to_hdf(fout, 'pdf', format='table')


#TODO: Design the class such that it can
class HDF5Read(object):
    def __init__(self, fin):
        self.fin = fin
        self.chunklog = 0

    def readCompressedChunk(self):
        self.chunklog += 1
        try:
            datachunk = pd.read_hdf(self.fin, pdfkey+str(self.chunklog))
            return datachunk
        except KeyError:
            return False


class HDF5Store(object):
    def __init__(self, fout):
        self.fout = fout
        self.chunklog = 0

    def storeCompressedChunk(self, pdDataFrame):
        self.chunklog += 1
        pdDataFrame.to_hdf(self.fout, pdfkey+str(self.chunklog), format='fixed')
