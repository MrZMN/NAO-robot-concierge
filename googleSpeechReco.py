#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.
"""

import re
import sys
from google.cloud import speech
import pyaudio
from six.moves import queue
import os

# this credential file should be manually downloaded from Google to enable speech-to-text API. Please follow the steps provided in official Google speech-to-text API website.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your_directory/your_certificate_name.json' 


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

transcript = ""
# As a concierge robot, we want it to make reactions when certain pre-defined keywords are recognised by Google Speech-to-text API, as shown in the flollowings:
global vocabulary
vocabulary = ["hello", "hi", "good morning", "good afternoon", "how are you", "now", "where am i", "stand up", "sit down", "dance", "bar", "robot battle event", "robot battery event", "thank you", "thanks", "sex", "6", "fix","bye", "goodbye", "story", "what can you do", "sounds good"]   # keywords
# The corresponding reaction logic to each keyword is defined in 'dialog.py'


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


class SpeechRecogniser(object):


    def __init__(self):
        self.language_code = "en-US"  # a BCP-47 language tag
        self.client = speech.SpeechClient()
        
        # configurations (Python 2 exclusive)
        self.config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=self.language_code,
        )
        self.streaming_config = speech.types.StreamingRecognitionConfig(
            config=self.config, interim_results=False
        )
    
    def run(self):
        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (
                speech.types.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = self.client.streaming_recognize(self.streaming_config, requests)  # Send the request
            
            self.listen_response(responses)    # Print transcription response
            
            return transcript   # return the transcript that contains keyword (to main.py)
            
    def listen_response(self, responses):
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            global transcript
            transcript = str(result.alternatives[0].transcript.strip()).lower()
	    
            print "Recognised:", transcript

            # Jump out the loop if keyword recognised
            if any(keyword in transcript for keyword in vocabulary):
                break

# Source: https://github.com/googleapis/python-speech/blob/main/samples/microphone/transcribe_streaming_mic.py