# AUDIO 3D TESTER 

This is a simple audio stereo manipulator in order to test some HRTF Kemar studies.
http://interface.cipic.ucdavis.edu/sound/tutorial/hrtf.html#KEMAR

My goal was to reproduce a small spatialization sensation avoiding machine learning and pre-trained situations.

Playing with some of the variables like delay, panning and decay it’s possible to achieve a small sensation of positioning of the audio source.

But in the end the mechanism is too fragile too be considered a valid one.

A possible future integration could be the integration of filters in order to reproduce the response of the ear’s pinna.


##USAGE

This tool requires kivy, numpy, pyaudio and the knob widget from kivy's garden.

	cd path_to_the_folder
	kivy main.py [mono_file.wav]



![alt tag](/sceenshot.png)
