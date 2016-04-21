import pandas as pd
import numpy as np
from setup import zlim
from HDF5manager import HDF5Read
from HDF5manager import pdfkey


def uncompress(filein, file_out):
    hdf5read = HDF5Read(filein)
    with pd.HDFStore(file_out) as HDFoutputStore:
        while True:
            read_in = hdf5read.readCompressedChunk()
            if read_in is False:
                break
            else:
                compressedDataFrame = compressChunk(read_in)

            HDFoutputStore.append(pdfkey, compressedDataFrame)


def compressChunk(dataChunk):
    densities = np.array(dataChunk['PDF_compressed'])
    lower_idx = np.array(dataChunk['compression_info_1'])
    higher_idx = np.array(dataChunk['compression_info_2'])
    compressedData = np.zeros((len(densities), len(zlim)))
    for i in range(len(densities)):
        compressedData[i, lower_idx[i]:higher_idx[i]] = densities[i]

    compressedDataFrame = pd.DataFrame(compressedData)
    return compressedDataFrame
