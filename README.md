# chuninect-py
A mysterious tool that detects things using Kinect v2.

⚠️ THIS IS A WORK IN PROGRESS! ⚠️ It only works with Brokenithm/ChuniIO as of the moment. KinectV1 support is planned.

# Requirements / Installation

A Kinect V2 (Kinect for Xbox One) with its USB adapter
- Kinect V1 (Xbox 360) is not supported as of the moment.

Python 3.4 or higher (I use Python 3.13)
- https://www.python.org/downloads/release/python-3132/

Kinect for Windows SDK v2:
- https://www.microsoft.com/en-us/download/details.aspx?id=44561

All python requirements should already be in requirements.txt. You can install it by executing `pip install -r requirements.txt`. 

For verbosity, here's the full list:
- pykinect2
  - https://github.com/JaeggiD/PyKinect2/tree/py312
  - Please use this version of pykinect2! The one in pyPI is outdated. You can manually install this by downloading that repository as a zip and running `pip install ./PyKinect2-py312.zip`. (but it should already be properly installed through the pip command we executed earlier)
- pygame
- pywin32

# How to Use
1. Clone/download the repository somewhere.
2. Run `pip install -r requirements.txt` if you haven't
3. Open Brokenithm Server
4. Run main.py

As of the moment, you have to manually change the depth min/max, sensor width/height and sensor position in [`main.py`](main.py). You should modify the depth max so that your background is fully black and not triggering the sensors.

# Contact
You may DM me through Discord: Kei @keikei14