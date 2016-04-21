"""Compression routines

"""

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as spl
from setup import zlim
from HDF5manager import HDF5Store
from setup import default_chunck
from transformData import getPDFinNumpyArray
from transformData import convertArrayPDFtoPandasCompressedPDF
from HDF5manager import readUncompressedPDF


class SplineCompression(object):

    def __init__(self, thresh):

        self.thresh = thresh

    def compress(self, file_in, file_out):
        HDFin = readUncompressedPDF(file_in, default_chunck)
        HDFout = HDF5Store(file_out)
        for el in HDFin:
            pdf_array, coadd_id = getPDFinNumpyArray(el)
            compressed_pdf = self.perform_compression(pdf_array)
            compr_data = convertArrayPDFtoPandasCompressedPDF(el, compressed_pdf, coadd_id)
            HDFout.storeCompressedChunk(compr_data)

    def perform_compression(self, data):
        """ Compress the PDF

        """
        simple_spline = np.array([])
        index_array = np.array([])
        for i in xrange(1, data.shape[1]):
            spline = spl(data[:, 0], data[:, i], ext=1)
            int_zw = spline(zlim)
            index_over = np.where(int_zw > self.thresh)[0]

            if len(index_over) < 2:
                print len(index_over)
                raise ValueError('The grid spacing is too big. This can happen for instance if the PDF resembles a delta function.')

            try:
                index_array = np.append(index_array,
                                        np.array([index_over[0], index_over[-1]]))
            except IndexError as e:
                print "Decrease the grid spacing! This can happen if the PDFs are a bit undersmoothed."
                print e.message
            data_over = np.array(int_zw[index_over[0]:index_over[-1]])
            simple_spline = np.append(simple_spline, data_over)
        return simple_spline, index_array
