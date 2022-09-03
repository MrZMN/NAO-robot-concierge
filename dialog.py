import main

# this file defines the robot's reaction when a certain keyword is recognised by speech recognition

class Dialog(object):

    def __init__(self, movemodule):
        self._movemodule = movemodule
        
    def answer(self, question):
        if "hello" in question or "hi" in question:
            return "Hello!"
        elif "how are you" in question:
            return "I'm good, thanks!"
        elif "good morning" in question:
            return "good morning"
        elif "good afternoon" in question:
            return "good afternoon"
        elif "nao" in question or "now" in question:
            return "Hi, I'm here!"
        elif "where am i" in question:
            return "We are at the superfloor of Melbourne Connect!"
        elif "bar" in question:
            return "Go straight"
        elif "robot battle event" in question or "robot battery event" in question:
            return "Go straight and turn left"
        elif "thank you" in question or "thanks" in question or "sex" in question or "6" in question or "fix" in question:
            return "You're welcome"    
        elif "bye" in question or "goodbye" in question:
            return "Bye"
        elif "story" in question:
            return "Once upon a time, there is a robot. Emmm, go to work and no story!" 
        elif "what can you do" in question:
            return "I can guide you the way and make you life easier. I can even dance!"
        elif "sounds good" in question:
            return "Thank you!" 
        elif "stand up" in question:
            self._movemodule.standUp()
            return
        elif "sit down" in question:
            self._movemodule.sitDown()
            return 
        elif "dance" in question:
            self._movemodule.hulaHoop()
            return 
        else:
            return "Sorry I didn't get you."
         
