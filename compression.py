"""Compression routines

"""

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as spl
from setup import zlim
from HDF5manager import ChunkedHDF5Store
from transformData import getPDFinNumpyArray
from transformData import convertArrayPDFtoPandasCompressedPDF
from HDF5manager import readUncompressedPDF


class SplineCompression(object):

    def __init__(self, thresh):

        self.thresh = thresh

    def compress(self, file_in, file_out):
        inPDF = readUncompressedPDF(file_in)
        HDFout = ChunkedHDF5Store(file_out)
        for PDFchunk in inPDF:
            pdf_array, coadd_id = getPDFinNumpyArray(PDFchunk)
            #print type(pdf_array)
            pdf_array = np.array(pdf_array, dtype='float16')
            compressed_pdf = self.perform_compression(pdf_array)
            compr_data = convertArrayPDFtoPandasCompressedPDF(PDFchunk, compressed_pdf, coadd_id)
            #print compr_data['PDF_compressed'].dtypes
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
                #raise ValueError('The grid spacing is too big. This can happen for instance if the PDF resembles a delta function.')
                continue

            try:
                index_array = np.append(index_array,
                                        np.array([index_over[0], index_over[-1]]))
            except IndexError as e:
                print "Decrease the grid spacing! This can happen if the PDFs are a bit undersmoothed."
                print e.message
            data_over = np.array(int_zw[index_over[0]:index_over[-1]])
            simple_spline = np.append(simple_spline, data_over)
            simple_spline = np.array(simple_spline, dtype='float16')
            index_array = np.array(index_array, dtype='uint8')
        return simple_spline, index_array
