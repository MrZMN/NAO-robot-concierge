import sys
import time

from naoqi import ALProxy
from naoqi import ALModule

memory = None

# this file enables the face detection ability by NAOQi

# NAPqi module
class FaceDetectModule(ALModule):


    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because we have our Python broker connected to NAOqi broker

        self.name = name
        self.tts = ALProxy("ALTextToSpeech")
        self.facetrack = ALProxy("ALFaceDetection")
        self.facetrack.setTrackingEnabled(True) 
        #print(self.facetrack.isTrackingEnabled())

        # Subscribe to the FaceDetected event (event name, module name, callback function name)
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("FaceDetected", self.name, "onFaceDetected")
        

    def onFaceDetected(self, *_args):
        """ Callback, This will be called each time a face is detected."""
        
        # Unsubscribe to the event when talking to avoid repetitions
        memory.unsubscribeToEvent("FaceDetected", self.name)

        self.tts.say("Hello friend!")
	time.sleep(1)

        # Subscribe again to the event
        #memory.subscribeToEvent("FaceDetected", "FaceDetectModule", "onFaceDetected")

    
#http://doc.aldebaran.com/2-1/dev/python/reacting_to_events.html#python-reacting-to-events
