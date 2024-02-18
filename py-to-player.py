#!/usr/bin/env 
import os
import random
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import pygame

def playaudio(id):
    try:
        pygame.mixer.music.load('/home/alexdonald/Music/' +str(id) + '.mp3')
        pygame.mixer.music.play()
        print("Playing: " + str(id))
    except Exception as e:
        print(e)

def shuffleaudio(id):
    try:
       print("play each file in the directory in a random order")
       # use random to play each file in the directory

       audio_files = [f for f in os.listdir('/home/alexdonald/Music/' +str(id)) if f.endswith(('.mp3'))]
       random.shuffle(audio_files)

       for audio_file in audio_files:
           file_path = '/home/alexdonald/Music/' +str(id) + '/' + audio_file
           pygame.mixer.music.load(file_path)
           pygame.mixer.music.play()
           while pygame.mixer.music.get_busy():
               continue
             
    except Exception as e:
        print(e)

def stopaudio():
    try:
        if pygame.mixer.music.get_busy() == True:
            pygame.mixer.music.stop()
            print("Pausing: " + str(id))
    except Exception as e:
        print(e)

def connect():
     try:
        os.system('echo "disconnect 44:3D:54:B9:30:55" | bluetoothctl')
        os.system('echo "connect 44:3D:54:B9:30:55" | bluetoothctl')
        os.system('pacmd set-default-sink bluez_sink.44_3D_54_B9_30_55.a2dp_sink')
     except Exception as e:
        print(e)

pygame.init()

while True:
    try:
        reader=SimpleMFRC522()

        # create a loop to scan tokens
        while True:
            print("Waiting for rfid to scan...")
            id= reader.read()[0]
            print("Card is:",id)
            if id == 584616865049: #helper card to connect to bluetooth
                connect()
                print("Connecting")
            elif id == 428997447724: #helper card to stop any audio playing
                stopaudio()
                print("Stopping audio")
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

