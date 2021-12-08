# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This simpletest example displays the Blink animation.
For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.
"""
import time

import board
import neopixel
import displayio
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.color import RED, GREEN, WHITE
from adafruit_funhouse.peripherals import Peripherals
from displayio_listselect import ListSelect
import foamyguy_nvm_helper as nvm_helper
from adafruit_display_text import bitmap_label
import terminalio

PREV_UP_STATE = False
PREV_DOWN_STATE = False
PREV_SELECT_STATE = False

CUR_ANIMATION_INDEX = 0
CUR_ANIMATION_NAME = "Cycle"

config_obj = {
    "index": 0,
    "name": "Cycle"
}


read_data = nvm_helper.read_data()
print("read data: ")
print(read_data)
if type(read_data) == dict:
    if "index" in read_data.keys() and "name" in read_data.keys():
        CUR_ANIMATION_INDEX = read_data["index"]
        CUR_ANIMATION_NAME = read_data["name"]
    else:
        nvm_helper.save_data(config_obj, test_run=False)

display = board.DISPLAY
# Make the display context
main_group = displayio.Group()
display.show(main_group)

fun_house = Peripherals()

animation_names = ["Cycle", "Chase", "Comet", "Rnbw Sprkle"]
list_select = ListSelect(
    scale=2,
    items=animation_names
)
list_select.selected_index = CUR_ANIMATION_INDEX
list_select.anchor_point = (0.5, 1.0)
list_select.anchored_position = (display.width // 2, display.height - 8)
main_group.append(list_select)


cur_playing_txt = bitmap_label.Label(terminalio.FONT, text=CUR_ANIMATION_NAME, scale=3)
cur_playing_txt.anchor_point = (0.5, 0)
cur_playing_txt.anchored_position = (display.width // 2, 8)
main_group.append(cur_playing_txt)

# Update to match the pin connected to your NeoPixels
pixel_pin = board.A0
# Update to match the number of NeoPixels you have connected
pixel_num = 30

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.25, auto_write=False)

colorcycle = ColorCycle(pixels, speed=0.4, colors=[GREEN, RED, WHITE])
chase = Chase(pixels, speed=0.1, color=GREEN, size=3, spacing=6)
comet = Comet(pixels, speed=0.05, color=RED, tail_length=10, bounce=True)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=5)

animations = [colorcycle, chase, comet, rainbow_sparkle]

while True:
    CUR_UP = fun_house.button_up
    CUR_DOWN = fun_house.button_down
    CUR_SELECT = fun_house.button_sel

    if CUR_UP and not PREV_UP_STATE:
        print("move selection up")
        list_select.move_selection_up()
    if CUR_DOWN and not PREV_DOWN_STATE:
        print("move selection down")
        list_select.move_selection_down()
    if CUR_SELECT and not PREV_SELECT_STATE:
        #print(list_select.selected_item)
        CUR_ANIMATION_INDEX = list_select.selected_index
        CUR_ANIMATION_NAME = list_select.selected_item
        config_obj["index"] = CUR_ANIMATION_INDEX
        config_obj["name"] = CUR_ANIMATION_NAME
        cur_playing_txt.text = CUR_ANIMATION_NAME
        print("saving: ")
        print(config_obj)
        nvm_helper.save_data(config_obj, test_run=False)

    PREV_UP_STATE = CUR_UP
    PREV_DOWN_STATE = CUR_DOWN
    PREV_SELECT_STATE = CUR_SELECT
    animations[CUR_ANIMATION_INDEX].animate()

    time.sleep(0.01)
