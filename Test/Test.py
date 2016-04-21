"""
Author MMRAU
"""

from SplineCompress.decompression import uncompress
from SplineCompress.compression import SplineCompression
from setup import thresh


#unit test
if __name__ == '__main__':
    in_file = 'test_output_new.hdf5'
    out_file = 'compressed_Y1A1_GOLD101_Y1A1trainValid_14.12.2015.validsY1A1.25215.out.DES.pdf.hdf5'
    test_spline_compression = SplineCompression(thresh)
    test_spline_compression.compress(in_file, out_file)
    uncompress(out_file, out_file+'reconstructed')
