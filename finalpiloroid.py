import RPi.GPIO as GPIO
from PIL import Image
import os, time, sys, picamera
from time import strftime
sys.path.append("/home/pi/Python-Thermal-Printer")
from Adafruit_Thermal import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT) # LED
GPIO.setup(26, GPIO.IN) # Button


#Flash LED to signal startup
GPIO.output(19,True)
time.sleep(0.1)
GPIO.output(19,False)
time.sleep(0.1)
GPIO.output(19,True)
time.sleep(0.1)
GPIO.output(19,False)
time.sleep(0.1)
GPIO.output(19,True)
time.sleep(0.1)
GPIO.output(19,False)

# define some variables
photoPath = "/home/pi/Documents/Piloroidpics/"
photoName = time.strftime("%b-%d-%Y^%H_%M_%S") + ".png"
photoResize = 512, 384
photoTitle = "Piloroid Photo"

#setup printer trying both USB ports
try:
	printer = Adafruit_Thermal("/dev/ttyUSB0", 9600, timeout=5)
except: # Try again with other USB port
	printer = Adafruit_Thermal("/dev/ttyUSB1", 9600, timeout=5)

#main loop which waits for button to press
try:
	while True:
		time.sleep(0.001) # do not use all the cpu power
		GPIO.setup(4, GPIO.OUT)
		
		if (GPIO.input(26)== True):
			when_pressed = time.time()

			while GPIO.input(26) == True:
				#wait until the button is not pressed any more
				time.sleep(0.001) # do not use all the cpu power
			#measure the length of time the button was pressed
			time_pressed = time.time() - when_pressed
				
			if time_pressed < 0.1:
				continue # pressed too short, ignore
				
			if 0.1 <= time_pressed < 3:
				#turn off LED to signal processing
				GPIO.output(19,False)

				# Take photo
				with picamera.PiCamera() as camera:
						camera.rotation=270
						camera.resolution=(800, 600)
						camera.sharpness=100
						camera.contrast=25
						camera.capture("/home/pi/Documents/Piloroidpics/" + photoName)   
						#os.system("sudo raspistill -p '144,48,512,384' --vflip -w 1920 -h 1440 --colfx 128:128 -o" + photoPath + photoName)

				#flash LED to notify of captured image
				GPIO.output(19,True)
				time.sleep(0.1)
				GPIO.output(19,False)
				
				# Resize the high res photo to create thumbnail
				Image.open(photoPath + photoName).resize(photoResize, Image.ANTIALIAS).save(photoPath + "thumbnail.jpg")
				# Rotate the thumbnail for printing
				Image.open(photoPath + "thumbnail.jpg").transpose(2).save(photoPath + "thumbnail-rotated.bmp")

				#print the photo
				try:
					printer.begin(210) # Warmup time
					#printer.setTimes(40000, 3000) # Set print and feed times
					printer.justify('C') # Center alignment
					printer.feed(1) # Add a blank line
					printer.printImage(Image.open(photoPath + "thumbnail-rotated.bmp"), True) # Specify thumbnail image to print
					printer.feed(10) # Add a few blank lines
					print("printed")
				except:
					print("Print Failed")
				
				#email photo
				try:
					os.system("mpack -s Yourphoto /home/pi/Documents/Piloroidpics/" + photoName + "your@email.com")
					print("Emailed!")
					#os.system("lp -o fit-to-page /home/pi/Documents/Piloroidpics/" + name + ".bmp")
				except:
					print("Picture Email Failed!\n")
				
				#delete thumbnail after printing
				os.remove(photoPath + "thumbnail-rotated.bmp")
				os.remove(photoPath + "thumbnail.jpg")
				print("Thumbnails deleted")
				
			if time_pressed <= 3:
				GPIO.setmode(GPIO.BCM)
				GPIO.setup(19, GPIO.OUT)

				#flash a bunch of times to signal shutdown
				for i in range(0,4):
					GPIO.output(19,True)
					time.sleep(0.1)
					GPIO.output(19,False)
					time.sleep(0.1)
				os.system("sudo shutdown now")

			#run emulationstation if button is held for a while
##            if time_pressed > 6:
##                GPIO.output(19,True)
##                time.sleep(2)
##                GPIO.output(19,False)
##                
##                os.system('emulationstation')
##        else:
##            GPIO.output(19,True)

finally:
	GPIO.cleanup()
