from naoqi import ALProxy
from naoqi import ALModule

# this file enables the speak ability by NAOQi

class SpeakModule(ALModule):

    def __init__(self, name, ip, port):
        ALModule.__init__(self, name)

        self.tts = ALProxy("ALTextToSpeech", ip, port)


    def say(self, speech):
        say_id = self.tts.post.say(speech)
        self.tts.wait(say_id, 0)  
        
#http://doc.aldebaran.com/2-1/dev/python/making_nao_speak.html#making-nao-speak
