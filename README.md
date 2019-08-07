## Piloroid
A Python script to run on a Raspberry Pi inside a polaroid camera to capture a photo with the Pi Cam, email the photo to the user, save on the SD card, and print the photo on a thermal printer.

## Background
Back in 2016 I got the idea that the classic Polaroid camera needed an update. I ordered a classic rainbow camera from eBay, hollowed it out, and isntalled a raspberry pi and thermal printer. 

## Physical components
The brain of the operation is the Raspberry Pi 3. I removed two of the USB ports so I could solder components directly to the PCB to save space.
The Pi cam integrates very easily with the camera with an easy to use Python module.
I used this [thermal printer](https://www.adafruit.com/product/597) from Adafruit which has a Python library made for it so it was pretty simple to setup.
I hid an LED inside the old exposure knob for user feedback
A simple on/off switch is added to the back of the camera to shut off power completely
A battery pack powered by 4 AA batteries was enough to power the pi but could not provide the current required of the printer so the prints were not very dark. This is what caused me to ultimately leave the project.
A new found experience with 18650 cells has me thinking about reviving the project and trying out these cells.

## How it works
1. Flick the switch on the back to turn on power
2. Wait for the LED to flash, indicating the camera is ready to go
3. Push the button to take a picture
   1. LED turns off to indicate processing
   2. Picture is taken
   3. Picture is saved to SD card
   4. LED Flashes once to indicate picture taken but still processing
   5. Image is converted to a thumbnail
   6. Image is printed
   7. While enjoying your new print, the picture is emailed to you is connected to a saved wifi network, like your phone's hotspot.
   8. Thumbnail is deleted
4. Hold button for more than 3 seconds to turn off Raspberry Pi safely
5. Bonus: Hold button for 6 seconds to run Emulation Station if installed

## Disclaimer
This project worked 3 years ago and I have no way of testing the code currently. Let me know of any changes you suggest.
