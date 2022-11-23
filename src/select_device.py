import inquirer
from inquirer import List

def select_device(pyaudio):
    info = pyaudio.get_host_api_info_by_index(0) # to Do: why 0? get default host?
    numdevices = info.get('deviceCount')
    devices = []
    
    for i in range(0, numdevices):
        deviceInfo = pyaudio.get_device_info_by_host_api_device_index(0, i)
        if (deviceInfo.get('maxInputChannels')) > 0:
            devices.append({
                "value": deviceInfo.get("index"),
                "name": deviceInfo.get("name"),
                "defaultSampleRate": int(deviceInfo.get("defaultSampleRate"))
            })
    
    answers = inquirer.prompt([
        List('device',
            message="Select an Audio Device",
            choices=devices,
        ),
    ])
    
    deviceId = answers["device"].get("value")
    sampleRate = answers["device"].get("defaultSampleRate")
    print("select " + answers["device"].get("name") + " with sample rate " + str(sampleRate) )
    
    return deviceId, sampleRate
                

