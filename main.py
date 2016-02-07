import kivy
kivy.require('1.8.0')
from kivy.config import Config
import kivy.garden
kivy.garden.garden_system_dir = '/Users/Sam/.kivy/garden'

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 350
SIZE_P = 10
SIZE_T = 10

import sys, math
#PYTHON PACKAGES IMPORT SU WINDOWS
#try: sys.path.append('C:\\Python27\\lib\\site-packages')
#except: pass


Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', str(WINDOW_WIDTH))
Config.set('graphics', 'height', str(WINDOW_HEIGHT))
Config.set('input', 'mouse','mouse,disable_multitouch')

from kivy.app import *
from kivy.uix.gridlayout import *
from kivy.uix.label import *
from kivy.uix.button import *
from kivy.uix.behaviors import *
from kivy.uix.widget import *
from kivy.properties import *
from kivy.graphics import *
from kivy.graphics.instructions import *
from kivy.input.motionevent import *
from kivy.event import *
from kivy.uix.layout import *
from kivy.lang import *
from kivy.clock import *
from kivy.core.window import *
from kivy.graphics.context import get_context
from kivy.uix.image import *
from kivy.uix.behaviors import *
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.graphics import Quad, Translate, Rotate, PushMatrix, PopMatrix
from kivy.graphics import Rectangle, Color, Callback, Rotate, PushMatrix, PopMatrix, Translate, Quad, Scale
from kivy.core.image import Image
from kivy.garden.knob import *
from kivy.uix.boxlayout import BoxLayout

from random import *
from Queue import *
from thread import *
from threading import *

import pyaudio
import time
import numpy as np
import wave


def ERROR_PROMPT(msg, method):
	print "\n[#### ERROR ####] | ",method, " | ", msg ,"\n"
	App.get_running_app().stop()


def WARING_PROMPT(msg, method):
	print "\n[#### WARNING ####] | ",method, " | ", msg ,"\n"



#############################################################################
#############################################################################
#############################################################################



knob_l='''
<single_knob>:
	min: 1
	max: 1000
	step: 1
	value: 1
	knobimg_source: "img/knob_black.png"
	marker_img: "img/bline3.png"
	knobimg_size: .8
	markeroff_color: 0, 0, 0, 0
	knobimg_color: 1, 1, 1, .5
	show_label: True
	show_marker: True

'''

class single_knob(Knob):

	def __init__(self,id, **kw):
		self.id = id
		Builder.load_string(knob_l)
		super(single_knob, self).__init__(**kw)


	def on_touch_down(self, touch):
		super(single_knob, self).on_touch_down(touch)
		if self.collide_point(*touch.pos):
			global l_p, r_p, l_d, r_d, l_t, r_t
			if touch.button == 'scrollup':
				if self.id == 'l_pan': 
					self.value += 1 
					l_p = round(self.value/1000,4)
				elif self.id == 'r_pan': r_p = round(self.value/1000,4)
				elif self.id == 'l_decay': l_d = round(self.value/1000,4)
				elif self.id == 'r_decay': r_d = round(self.value/1000,4)
				elif self.id == 'l_time': l_t = round(self.value/10000,4)
				elif self.id == 'r_time': r_t = round(self.value/10000,4)
		


	def on_touch_move(self, touch):
		super(single_knob, self).on_touch_move(touch)

		if self.collide_point(*touch.pos):

			global l_p, r_p, l_d, r_d, l_t, r_t
			print '\rmove ', self.id, " >>> ", round(self.value/1000,4),
			if self.id == 'l_pan': l_p = round(self.value/1000,4)
			elif self.id == 'r_pan': r_p = round(self.value/1000,4)
			elif self.id == 'l_decay': l_d = round(self.value/1000,4)
			elif self.id == 'r_decay': r_d = round(self.value/1000,4)
			elif self.id == 'l_time': l_t = round(self.value/10000,4)
			elif self.id == 'r_time': r_t = round(self.value/10000,4)
	

grid='''
<sp3d_layout>
	canvas:
		Color:
			rgba: .8,.6,.0,.5
		Line:
			points: 175, 80, 175, 580
			width: 2
'''

class sp3d_layout(GridLayout):

	def __init__(self, **kw):
		Builder.load_string(grid)
		super(sp3d_layout, self).__init__(**kw)
		self.rows = 6
		self.cols = 2
		self.spacing = [50, 30]
		self.padding = [50, 50, 50, 50]
		self.l_decay = single_knob('l_decay')
		self.l_time = single_knob('l_time')
		self.r_decay = single_knob('r_decay')
		self.r_time = single_knob('r_time')
		self.r_pan = single_knob('r_pan')
		self.r_pan.value = 1000
		self.l_pan = single_knob('l_pan')
		self.l_pan.value = 1000

		self.add_widget(self.l_decay)
		self.add_widget(self.r_decay)
		self.add_widget(Label(text="Left Decay"))
		self.add_widget(Label(text="Right Decay"))

		self.add_widget(self.l_time)
		self.add_widget(self.r_time)
		self.add_widget(Label(text="Left Delay (ms)"))
		self.add_widget(Label(text="Right Delay (ms)"))

		self.add_widget(self.l_pan)
		self.add_widget(self.r_pan)
		self.add_widget(Label(text="Left Volume"))
		self.add_widget(Label(text="Right Volume"))


class action(Button):

	def __init__(self,id,stream, f,**kw):
		super(action, self).__init__(**kw)
		self.text = id
		self.background_color = (.8,.6,.0,1)
		self.stream = stream
		self.f = f

	def on_press(self,**kw):
		super(action, self).on_press(**kw)
		if(self.text == 'PLAY' and not self.stream.is_active()):
			self.stream.start_stream()
		elif(self.text == 'PAUSE' and self.stream.is_active()):
			self.stream.stop_stream()
		elif(self.text == 'STOP' and self.stream.is_active()):
			self.stream.stop_stream()
			self.f.rewind()
			global buf_l, buf_r
			buf_l = np.empty(0,dtype='Int16')
			buf_r = np.empty(0,dtype='Int16')

	





class buttonBar(BoxLayout):

	def __init__(self,stream, f, **kw):
		super(buttonBar, self).__init__(**kw)
		self.orientation = 'horizontal'
		self.play_button = action('PLAY',stream, f)
		self.stop_button = action('STOP',stream, f)
		self.pause_button = action('PAUSE',stream, f)

		self.add_widget(self.play_button)
		self.add_widget(self.stop_button)
		self.add_widget(self.pause_button)


class mainLayout(BoxLayout):

	def __init__(self,stream, f, **kw):
		super(mainLayout, self).__init__(**kw)
		global path
		self.orientation = 'vertical'
		self.controls = sp3d_layout()
		self.buttons = buttonBar(stream,f)
		self.controls.size_hint = (1,.9)
		self.file_name = Label(text=path)
		self.file_name.size_hint = (1,.03)
		self.buttons.size_hint = (1,.07)
		self.add_widget(self.controls)
		self.add_widget(self.file_name)
		self.add_widget(self.buttons)




class sp3d(App):

	def __init__(self,stream,f,**kw):
		super(sp3d, self).__init__(**kw)
		self.f = f
		self.stream = stream

	def build(self, **kw):
		super(sp3d, self).build(**kw)
		
		return mainLayout(self.stream, self.f)


if __name__ == "__main__":
	
	buf_l = np.empty(0,dtype='Int16')
	buf_r = np.empty(0,dtype='Int16')
	l_d = .1
	r_d = .1
	l_t = .1
	r_t = .1
	l_p = 1
	r_p = 1

	path = 'bach_mono.wav'
	if len(sys.argv) > 1:
		path = sys.argv[1]

	try: 
		f = wave.open(path,'rb')
	except:
		try:
			WARING_PROMPT("CANNOT OPEN " + sys.argv[1] +" FALLBACK ON BACH.WAV","__main__")
			f = wave.open('bach_mono.wav','rb')

		except:
			ERROR_PROMPT("WHERE THE FUCK IS BACH!!!!", "__main__")
			sys.exit(0)


	p = pyaudio.PyAudio()

	def callback(in_data, frame_count, time_info, status):
		global l_p, r_p, l_d, r_d, l_t, r_t, buf_l, buf_r
		data = f.readframes(frame_count)


		if len(data) < frame_count/2: 
			f.rewind()
			data = f.readframes(frame_count)

		data = np.fromstring(data, 'Int16')
		decoded = np.ravel(np.column_stack((data,data)))


		decoded[::2] = np.multiply(decoded[::2], l_p)
		decoded[1::2] = np.multiply(decoded[1::2], r_p)
		
		if (buf_l.size)/44100. >= l_t:
			decoded[::2] = np.add(decoded[::2], np.multiply(buf_l[:decoded.size/2], l_d))
			buf_l = buf_l[decoded.size/2:]

		if (buf_r.size)/44100. >= r_t:
			decoded[1::2] = np.add(decoded[1::2], np.multiply(buf_r[:decoded.size/2], r_d))
			buf_r = buf_r[decoded.size/2:]

		buf_l = np.concatenate((buf_l,decoded[::2]),axis = 0)
		buf_r = np.concatenate((buf_r,decoded[1::2]),axis = 0)
	
	
		np.clip(decoded, np.iinfo(np.int16).min, np.iinfo(np.int16).max)

		out = decoded.astype(np.int16).tostring()
		return (out, pyaudio.paContinue)

	try:  
		stream = p.open(format = pyaudio.paInt16,  
						channels = 2,  
						rate = f.getframerate(),  
						output = True,
						stream_callback = callback)
	except:
		ERROR_PROMPT("CANNOT CREATE STREAM.", "__main__")

	stream.stop_stream()  
	sp3d(stream, f).run()
	

	stream.close()  
	p.terminate() 


