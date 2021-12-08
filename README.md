### Required libraries:
- https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation
- https://github.com/adafruit/Adafruit_CircuitPython_FunHouse
- https://github.com/adafruit/Adafruit_CircuitPython_Neopixel
- https://github.com/FoamyGuy/CircuitPython_Org_DisplayIO_ListSelect
- https://github.com/FoamyGuy/Foamyguy_CircuitPython_nvm_helper

# Persistent LED Animation Selector

This example runs on the Adafruit FunHouse and allows you to select one of 4 different LED animations. 

The selected animation is stored persistently in NVM storage and retrieved again whenever `code.py` runs.

It will continue playing the most recently selected animation upon booting up and launching `code.py`.

The primary purpose of the example is to show how to use the NVM_Helper library to store application state or configuration information and act upon the stored information when `code.py` is run.
