from naoqi import ALModule
from naoqi import ALProxy
import time

memory = None

# this file enables the speech recognition ability by NAOQi

class SpeechRecoModule(ALModule):
    ENABLE_WORD_SPOTTING = False
    CONFIDENCE_THRESHOLD = 20	#Confidence threshold (%)
    
    def __init__(self, name, vocabulary):
        ALModule.__init__(self, name)
        
        self.name = name
        
        self.tts = ALProxy("ALTextToSpeech")
	
        self.asr = ALProxy("ALSpeechRecognition")
        self.asr.pause(True)
        self.asr.setVocabulary(vocabulary.split(';'), self.ENABLE_WORD_SPOTTING)
        self.asr.pause(False)
        
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("WordRecognized", self.name, "onWordRecognized")
        

	# callback. value -> [phrase_1, confidence_1, phrase_2, confidence_2, ...] (ranked by condifence)
    def onWordRecognized(self, eventName, value, subscriberIdentifier):
        
        memory.unsubscribeToEvent("WordRecognized", self.name)
        
        if value[1] >= self.CONFIDENCE_THRESHOLD / 100. :
            self.Dialog(value[0])  
        else:
            print("nothing recognized")
            
        time.sleep(1)
        memory.subscribeToEvent("WordRecognized", self.name, "onWordRecognized")
        
        
    # robot reaction to recognised word
    def Dialog(self, word):

        print("this is recoqnized: " + word)
        
        global say_id
        
        if ("hello" in word or "hi" in word):
        	say_id = self.tts.post.say("Oh hello!")
        elif "how are you" in word:
        	say_id = self.tts.post.say("I'm good!")
        elif "good morning" in word:
        	say_id = self.tts.post.say("Good morning!")
        elif "nao" in word:
            say_id = self.tts.post.say("Hi, I'm here!")
        elif "where am I" in word:
            say_id = self.tts.post.say("We are in the I X T lab!")
					
        self.tts.wait(say_id, 0)


#https://github.com/salaxy/NaoSimpleSpeechRecognition/blob/master/src/speech_test_improve.py
