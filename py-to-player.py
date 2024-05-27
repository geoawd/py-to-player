#!/usr/bin/env 
import os
import random
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import pygame

def disconnect_all():
    try:
        # List all connected devices
        result = os.popen('bluetoothctl paired-devices').read()
        devices = result.split('\n')
        
        for device in devices:
            if 'Device' in device:
                # Extract the device ID
                device_id = device.split(' ')[1]
                # Disconnect the device
                os.system(f'echo "disconnect {device_id}" | bluetoothctl')
    except Exception as e:
        print(f"Error during disconnecting: {e}")

def connect(id):
    try:
        # Disconnect all connected devices
        disconnect_all()
        
        # Connect to the new device
        os.system(f'echo "connect {id}" | bluetoothctl')
        os.system(f'pacmd set-default-sink bluez_sink.{id}.a2dp_sink')
    except Exception as e:
        print(e)

def playaudio(id):
    try:
        pygame.mixer.music.load('/home/alexdonald/Music/' +str(id) + '.mp3')
        pygame.mixer.music.play()
        print("Playing: " + str(id))
    except Exception as e:
        print(e)

def shuffleaudio(id):
    try:
       audio_files = [f for f in os.listdir('/home/alexdonald/Music/' +str(id)) if f.endswith(('.mp3'))]
       random.shuffle(audio_files)

       for audio_file in audio_files:
           file_path = '/home/alexdonald/Music/' +str(id) + '/' + audio_file
           pygame.mixer.music.load(file_path)
           pygame.mixer.music.play()
             
    except Exception as e:
        print(e)

class Pause(object):

    def __init__(self):
        self.paused = pygame.mixer.music.get_busy()

    def toggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
        if not self.paused:
            pygame.mixer.music.pause()
        self.paused = not self.paused

pygame.init()

pause = Pause()

while True:
    try:
        reader=SimpleMFRC522()

        # create a loop to scan tokens
        while True:
            print("Waiting for rfid to scan...")
            id= reader.read()[0]
            print("Card is:",id)
            if id == 584616865049: #helper card to connect to echo dot
                connect('44:3D:54:B9:30:55')
                print("Connecting to echo dot")
            elif id == 584616865050: #helper card to connect to headphones
                connect('47:0C:90:0B:86:3A')
                print("Connecting to headphones")
            elif id == 428997447724: #helper card to pause/resume music
                pause.toggle()
            elif os.path.isfile('/home/alexdonald/Music/' +str(id) + '.mp3'):
                playaudio(id)
            elif os.path.isdir('/home/alexdonald/Music/' +str(id)):
                print("Directory - shuffling audio in this directory") 
                shuffleaudio(id)
            else:
                print("Nothing to play")
    except Exception as e:
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
