import sys
import signal
import numpy
import pyaudio
import asyncio
import websockets
import json

sys.path.append("src")
from select_device import select_device
from find_freq_indicies import find_freq_indicies
from magnitude_to_decibel import magnitude_to_decibel
sys.path.remove("src")

# Websocket listen to
URL = "localhost"
PORT = 8666

p = pyaudio.PyAudio()
CHUNK = 2**11

# Select Input Device and Open PyAudio Stream
deviceId, sampleRate = select_device(p)
stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                rate = sampleRate,
                input = True,
                frames_per_buffer = CHUNK,
                input_device_index = deviceId)

print("starting...")
# Init shutdown process on Ctrl+C 
def handle_close(signum, frame):
    print("\nStopping")
    stream.close()
    p.terminate()
    exit(1)
signal.signal(signal.SIGINT, handle_close)

coefficients = numpy.fft.fftfreq(CHUNK)
frequencies = [ numpy.abs(c * sampleRate) for c in coefficients ]

bass_start, bass_end        = find_freq_indicies([40, 140], frequencies)      # bass ~40-140Hz
lowMid_start, lowMid_end    = find_freq_indicies([140, 400], frequencies)     # lowMid ~140-400Hz
mid_start, mid_end          = find_freq_indicies([400, 2600], frequencies)    # mid ~400-2600Hz
highMid_start, highMid_end  = find_freq_indicies([2600, 5200], frequencies)   # highMid ~2600-5200Hz
treble_start, treble_end    = find_freq_indicies([5200, 14000] , frequencies) # treble ~5200-1400Hz

async def ws_stream(websocket, path):
    print("opened connection")
    # Listen to Sound Input
    while True:
        data_buffer = stream.read(CHUNK, exception_on_overflow=False)
        sound_data = numpy.frombuffer(data_buffer, dtype=numpy.int16)
        
        numpy_fft = numpy.fft.fft(sound_data)
        magnitudes = numpy.abs(numpy_fft).astype(int)
        decibels = magnitude_to_decibel(magnitudes)

        # MAX values
        bass_max    = numpy.max(decibels[bass_start:bass_end]).astype(int)
        lowMid_max  = numpy.max(decibels[lowMid_start:lowMid_end]).astype(int)
        mid_max     = numpy.max(decibels[mid_start:mid_end]).astype(int)
        highMid_max = numpy.max(decibels[highMid_start:highMid_end]).astype(int)
        treble_max  = numpy.max(decibels[treble_start:treble_end]).astype(int)

        # MEAN values
        # bass_mean    = numpy.mean(decibels[bass_start:bass_end], dtype=numpy.int16)
        # lowMid_mean  = numpy.mean(decibels[lowMid_start:lowMid_end], dtype=numpy.int16)
        # mid_mean     = numpy.mean(decibels[mid_start:mid_end],  dtype=numpy.int16)
        # highMid_mean = numpy.mean(decibels[highMid_start:highMid_end], dtype=numpy.int16)
        # treble_mean  = numpy.mean(decibels[treble_start:treble_end], dtype=numpy.int16)
        
        ws_msg = json.dumps({
            "bass":     int(bass_max),
            "lowMid":   int(lowMid_max),
            "mid":      int(mid_max),
            "highMid":  int(highMid_max),
            "treble":   int(treble_max)
        })
        
        # Send WS Message
        try:
            await websocket.send(ws_msg)
        except websockets.exceptions.ConnectionClosed:
            print("connection closed")
            break

# Run Websocket Server
start_server = websockets.serve(ws_stream, URL, PORT)
print("server running. use ctrl+c to stop")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

