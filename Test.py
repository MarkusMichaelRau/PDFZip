"""
Author MMRAU
"""

from decompression import uncompress
from compression import SplineCompression
from setup import thresh


#unit test
if __name__ == '__main__':
    in_file = '/Volumes/NeutronStar/PDFZipTest/PHOTOZ_ADA_Z_Y1_v0.3.hdf5'
    out_file = '/Volumes/NeutronStar/PDFZipTest/PHOTOZ_ADA_Z_Y1_v0.3.hdf5compressed'
    test_spline_compression = SplineCompression(thresh)
    test_spline_compression.compress(in_file, out_file)
    uncompress(out_file, out_file+'reconstructed')
