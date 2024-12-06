import sys
import time
import os
import threading
import mido
from pygame import mixer
from main_display_write import NoteDisplay
from main_play import Sampler
import datetime
is_green: bool = True
notes_on: list = []
sampler: Sampler = None
note_ui: NoteDisplay = None

note_ui = NoteDisplay(button_record_callback, button_replay_callback, button_stop_callback, combo_select)







def learn(mid_part):

    