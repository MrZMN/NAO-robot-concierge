# NAO_concierge
Concierge robot of the superfloor of Melbourne Connect at the University of Melbourne. Based on SoftBank NAO robot.

### What can it do?
This project enables several core fuctions of a robot: speech recognition, movement, speak, work with GUI, etc.

### What do you need in advance?
1. A NAO robot and a computer. Make sure they are connected to the **same** network.
2. NAOQi Python SDK installed. At the moment of Aug 2022, the NAOQi SDK only supports Python 2.
3. (Optional) Google speech-to-text API set.
4. External Python libraries installed, such as (not limited to) zmq to enable lightweight client-server communication, pyaudio to enable microphone control, and PyQt4 to enable GUI (PyQt5 doesn't support Python 2).

To test if you have NAOQi Python SDK installed, you can run 
```python
from naoqi import ALProxy
```
in Python 2 and see if it works properly.

You can use multiple ways to realise speech recognition. You can directly use the module provided by NaoQi (speechReco.py), or you can use Google speech-to-text API (like this project). In order to do this, you need to first enable Google speech-to-API using your own account, and insert your credential file into this project (your_certificate_name.json). Please refer to the official Google website for detailed steps.

The rest of involved Python libraries should be installed while enabling Google speech-to-text API.

You do *not* need ROS enabled.

### The last steps to run the project
Since you have set the environment, you can run the project by:
1. Get the robot's IP address by pressing the chest button. Put the IP address in the 'main.py' file.
2. Run **both** 'main.py' and 'userInterface.py' using **Python 2**.
3. As a back end, you can also run 'conciergeInterface.py' to alter the user GUI.

### Others
Relevant comments are added in each Python file to assist you from understanding the logic.
If you get any questions, feel free to email: mo.zhang1919219@gmail.com
