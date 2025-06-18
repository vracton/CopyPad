import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.modules.encoder import EncoderHandler
from kmk.modules.oled import Oled, OledDisplayMode, OledReactionType, OledReaction
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC

from adafruit_display_text import label
import displayio
import terminalio

keyboard = KMKKeyboard()

key_pins = (board.D1, board.D2, board.D3)
keyboard.matrix = KeysScanner(pins=key_pins, value_when_pressed=False, pull=True)

keyboard.extensions.append(MediaKeys())

encoder = EncoderHandler()
encoder.pins = ((board.D4, board.D5, None),)
encoder.map = [((KC.VOLD, KC.VOLU),)]
keyboard.modules.append(encoder)

oled = Oled(128, 32, flip=False)

current_action = "Your Move"

def draw_oled(oled_obj, display):
    global current_action
    text = label.Label(terminalio.FONT, text=current_action, scale=1)
    text.anchor_point = (0, 0)
    text.anchored_position = (0, 0)
    display.append(text)

def onXPress(key, keyboard, *args):
    global current_action
    current_action = "Cut"
    keyboard.modules[1].update_display()
    keyboard.tap_key(KC.LCTRL(KC.X))
    return False

def onCPress(key, keyboard, *args):
    global current_action
    current_action = "Copied"
    keyboard.modules[1].update_display()
    keyboard.tap_key(KC.LCTRL(KC.C))
    return False

def onVPress(key, keyboard, *args):
    global current_action
    current_action = "Pasted"
    keyboard.modules[1].update_display()
    keyboard.tap_key(KC.LCTRL(KC.V))
    return False

oled.reactions = [OledReaction(OledReactionType.ON_BOOT, draw_oled)]
oled.display_mode = OledDisplayMode.MANUAL
keyboard.modules.append(oled)

X_KEY = KC.X.clone()
X_KEY.before_press_handler(onXPress)

C_KEY = KC.C.clone()
C_KEY.before_press_handler(onCPress)

V_KEY = KC.V.clone()
V_KEY.before_press_handler(onVPress)

keyboard.keymap = [
    [
        X_KEY, C_KEY, V_KEY
    ]
]

if __name__ == '__main__':
    keyboard.go()