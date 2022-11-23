import numpy

# @input magnitues: absolute values of FFT 
# @return according DB values
# db = 20 * log10(magnitude);
def magnitude_to_decibel(magnitudes):
    
    for i in range(len(magnitudes)):
        if magnitudes[i] > 0:
            magnitudes[i] = 20 * numpy.log10(magnitudes[i])
            
    return magnitudes
