import pandas as pd

_chunksize = 10000
pdfkey = 'pdf'
pointpredkey = 'pointpred'


def readUncompressedPDF(fname):
    return pd.read_hdf(fname, pdfkey, chunksize=_chunksize)


def readAdditionalFields(fname):
    return pd.read_hdf(fname, pointpredkey, chunksize=_chunksize)


def writeUncompressedPDF(fout, pdDataFrame):
    pdDataFrame.to_hdf(fout, 'pdf', format='table', complevel=5, complib='blosc:snappy')


#TODO: Design the class such that it can
class ChunkedHDF5Read(object):
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


class ChunkedHDF5Store(object):
    def __init__(self, fout):
        self.fout = fout
        self.chunklog = 0

    def storeCompressedChunk(self, pdDataFrame):
        self.chunklog += 1
        pdDataFrame.to_hdf(self.fout, pdfkey+str(self.chunklog), format='fixed', complevel=5, complib='blosc')
