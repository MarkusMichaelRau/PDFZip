import pandas as pd
import numpy as np
from setup import zlim
from HDF5manager import ChunkedHDF5Read
from HDF5manager import pdfkey


def uncompress(filein, file_out):
    hdf5read = ChunkedHDF5Read(filein)
    with pd.HDFStore(file_out) as HDFoutputStore:
        while True:
            read_in = hdf5read.readCompressedChunk()
            if read_in is False:
                break
            else:
                uncompressedDataFrame = uncompressChunk(read_in)

            HDFoutputStore.append(pdfkey, uncompressedDataFrame, complevel=5, complib='blosc:snappy')
            #HDFoutputStore.append('COADD_ID', read_in['COADD_OBJECTS_ID'], complevel=5, complib='blosc:snappy')


def uncompressChunk(dataChunk):
    #coaddID = dataChunk['COADD_OBJECTS_ID']
    densities = np.array(dataChunk['PDF_compressed'])
    lower_idx = np.array(dataChunk['compression_info_1'])
    higher_idx = np.array(dataChunk['compression_info_2'])
    uncompressedData = np.zeros((len(densities), len(zlim)))
    for i in range(len(densities)):
        uncompressedData[i, lower_idx[i]:higher_idx[i]] = densities[i]

    uncompressedDataFrame = pd.DataFrame(uncompressedData)
    #print len(uncompressedDataFrame.index)
    #uncompressedDataFrame.columns = ['pdf_%s' % c for c in uncompressedDataFrame.columns]
    #uncompressedDataFrame['COADD_OBJECTS_ID'] = coaddID
    #print uncompressedDataFrame.dtypes
    return uncompressedDataFrame
