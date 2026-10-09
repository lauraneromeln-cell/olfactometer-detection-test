Clinical Olfactometer – Arduino and Python Control Software
This repository contains the control software of the olfactometer described in the article:
"Design, fabrication and assembly of a clinical olfactometer for early Alzheimer's detection"
by DESPRES Elodie, NEROME Laura, SAADI Isma.
It was created as a complement to the article, as part of a scientific project at SupBiotech, a biotechnology engineering school in Paris. The project, on the theme of olfaction and cognition, aims to build an olfactometer that can be used for tests of smell loss, which is linked to Alzheimer's disease.
> *NB* : The code in this repository is only one part of the device. The rest of the olfactometer (design, materials, assembly and methods) is described in the article. This software is a research prototype and is not a certified medical device.
> 
What is in this repository
File	Description
`olfactometer.ino`	Arduino firmware. It receives commands from the computer and opens or closes the valves.
`olfactometer_gui.py`	Python graphical interface. It is used by the experimenter to control the device and record the answers.
> 
How it works
The olfactometer has 4 channels: three odors (peppermint, rose, cinnamon) and one blank (blank air). Peppermint is used as the control odor.
The experimenter enters the participant's information and chooses an odor in the Python interface.
When the sequence is started, the interface sends commands to the Arduino through the serial port.
The Arduino opens the valve of the chosen odor. Only one valve can be open at a time.
After the odor time, the blank channel is opened to clean the system. Then all valves are closed.
The participant says if the odor was detected. The experimenter push YES or NO, and the answer is saved in an excel file.
The default times are set but they can be changed in the interface.
The interface uses a blue and orange color palette, so it can be used by color-blind people.
> 
Requirements
An Arduino board connected to the computer by USB, with the valves wired as described in the article
Arduino IDE
Python 3
The `pyserial` library: `pip install pyserial`
Valve pins: peppermint = 7, rose = 5, cinnamon = 4, blank = 3.

Installation and use
1. Upload `olfactometer.ino` to the Arduino board with the Arduino IDE.
2. Install the Python library: `pip install pyserial`.
3. In `olfactometer_gui.py`, set `ARDUINO_PORT` to the COM port of your Arduino.
4. Run the interface: `python olfactometer_gui.py`.

If no Arduino is detected, the interface starts in demo mode (no command is sent to the valves).

Data recording
One CSV file is created for each participant in the `Documents` folder, with the name `Record_LASTNAME_Firstname.csv`. It contains the participant's information, then the answers (time, odor detected or not).

Citation
If you use this code, please cite the article:
> DESPRES Elodie, NEROME Laura, SAADI Isma. Design, fabrication and assembly of a clinical olfactometer for early Alzheimer's detection. 2028
Contact
NEROME Laura lauranerome.ln@gmail.com
