# py-to-player
A raspberry pi, RFID controlled, audio player for children

The aim is to create a music/audio book player that will play local files when triggered with an RFID card/sticker. The output device is an existing Amazon Alexa that will be connected with Bluetooth.

These are mostly notes so that I can recall the steps to recreate this project if I need to.

## Equipment list
- Raspberry Pi zero W
- RC522 RFID
- NTAG-213 stickers
- Amazon Alexa Dot

## Raspberry Pi configuration
I used a pi zero w as this was readibly available with the header already soldered.
- enable SPIO
- disable defualt audio (the HDMI, that I do not want to use)
  
Setting the audio out to use the bluetooth speaker is slightly trickier. After pairing the speaker in the GUI I tried to set a default config in
/etc/pulse/client.conf.

Identify the audio sinks using
- pacmd list-sinks

As the defauly config proved unreliable, I have a shell script that launches on boot via the cron tab (sudo crontab -e)

@reboot sh /launch.sh

launch.sh contains the following.
- echo "disconnect 44:3D:54:B9:30:55" | bluetoothctl 
- echo "connect 44:3D:54:B9:30:55" | bluetoothctl
- pacmd "set-default-source bluez_sink.44_3D_54_B9_30_55.a2dp_sink.monitor"

With these settings, the Raspberry Pi will connect to the Alexa on reboot.

## Python environment
To make this work we need to use the library for the RFID reader. I used https://github.com/pimylifeup/MFRC522-python
I don't need to be able to write to the RDIF stickers as I'm only using the NTAG-213 stickers to read the ID and use this to determine what audio to play. This allows me to use the NTAG-213 stickers that you get lots of on Amazon/ebay for just a few £.

## Playing the audio
To play the audio you tap the RFID with the NTAG-213 sticker. To make this easy, we stuck these on the barcodes of the books that we had recorded audio for.
We also created some custom cards using a MIFARE RFID card that were decorated to identify what would be played.



