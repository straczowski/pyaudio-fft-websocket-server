
# @input freq_range: is list of length 2, first element is start, second is end of desired range
# @input freqs: should be the result of numpy.fft.fftfreq
# @return indicies where it find start and end in array
def find_freq_indicies(freq_range, freqs):
    start = freq_range[0]
    end = freq_range[1]
    start_idx = -1
    end_idx = -1
    for i, freq in enumerate(freqs):
        if (freq >= start) and (start_idx < 0):
            start_idx = i 
        if (freq >= end) and (end_idx < 0):
            end_idx = i 
        if (start_idx >= 0) and (end_idx >= 0):
            break
    return start_idx, end_idx

