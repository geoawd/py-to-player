# py-to-player
A raspberry pi, RFID controlled, audio player for children

The aim is to create a music/audio book player that will play local files when triggered with an RFID card/sticker. The output device is an existing Amazon Alexa that will be connected with Bluetooth.

## Equipment list
- Raspberry Pi zero W
- RC522 RFID
- NTAG-213 stickers
- Amazon Alexa Dot

## Raspberry Pi configuration
I used a pi zero w as this was readibly available with the header already soldered.
- enable SPIO

- pacmd list-sources
- pacmd list-sinks

Setting the audio out to use the bluetooth speaker is slightly trickier. After pairing the speaker in the GUI I tried to set a default config in
/etc/pulse/client.conf but this wasn't very stable.

To get around this, I have a shell script that launches on boot via the cron tab

@reboot sh /launch.sh

launch.sh contains the following.
- echo "disconnect 44:3D:54:B9:30:55" | bluetoothctl
- echo "connect 44:3D:54:B9:30:55" | bluetoothctl
- pacmd "set-default-source bluez_sink.44_3D_54_B9_30_55.a2dp_sink.monitor"

## Python environment

import mfrc522
