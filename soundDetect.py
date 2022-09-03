import sys
import time
from naoqi import ALProxy
from naoqi import ALModule

memory = None

# this file enables the sound detection ability by NAOQi

class SoundDetectModule(ALModule):


    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because we have our Python broker connected to NAOqi broker

        self.name = name

        self.tts = ALProxy("ALTextToSpeech")
        self.sd = ALProxy("ALSoundDetection")
        self.sd.setParameter("Sensitivity", 0.8)

        # Subscribe to the SoundDetected event (event name, module name, callback function name)
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("SoundDetected", self.name, "onSoundDetected")
        

    def onSoundDetected(self, *_args):
        """ Callback"""
        
        # Unsubscribe to the event when talking to avoid repetitions
        memory.unsubscribeToEvent("SoundDetected", self.name)

        self.tts.say("Oh! I hear something!")

        # Subscribe again to the event
        memory.subscribeToEvent("SoundDetected", self.name, "onSoundDetected")

