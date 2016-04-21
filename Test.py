"""
Author MMRAU
"""

from decompression import uncompress
from compression import SplineCompression
from setup import thresh


#unit test
if __name__ == '__main__':
    in_file = './Test/test_output_new.hdf5'
    out_file = './Test/compressed_Y1A1_GOLD101_Y1A1trainValid_14.12.2015.validsY1A1.25215.out.DES.pdf.hdf5'
    test_spline_compression = SplineCompression(thresh)
    test_spline_compression.compress(in_file, out_file)
    uncompress(out_file, out_file+'reconstructed')
