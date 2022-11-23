# pyaudio-fft-websocket-server

Takes PyAudio stream, analyses frequency ranges with FFT, serves data through websocket.

opens port on `localhost:8666`

*Example Output*
```
{"bass": 98, "lowMid": 82, "mid": 76, "highMid": 58, "treble": 55}
```

## Required Packages

1. [portaudio](https://pypi.org/project/PyAudio/)
2. [inquirer](https://pypi.org/project/inquirer/)
3. [numpy](https://pypi.org/project/numpy/)
4. [websockets](https://pypi.org/project/websockets/)

# Run

```
python app.py
```

Prompt will ask you to select audio input device

```
[?] Select an Audio Device: {'value': 0, 'name': 'BlackHole 2ch', 'defaultSampleRate': 44100}
 > {'value': 0, 'name': 'BlackHole 2ch', 'defaultSampleRate': 44100}
   {'value': 1, 'name': 'MacBook Pro Mikrofon', 'defaultSampleRate': 48000}
   {'value': 3, 'name': 'Microsoft Teams Audio', 'defaultSampleRate': 48000}
```

webser is ready to serve!

```
server running. use ctrl+c to stop
```

*Note* there is no further logging during FFT analysis or streaming, to stay performant as possible

