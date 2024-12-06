import sys
import time
import os
import threading
import mido
from pygame import mixer
from main_display_write import NoteDisplay
from main_play import Sampler
import datetime
is_stopped = False
recorded_notes: list = []  
is_recording: bool = False
is_green: bool = True
last_note = []
notes_on: list = []
start_time: float = None
sampler: Sampler = None
n_list: dict = {}
n_off_list: dict = {}
note_ui: NoteDisplay = None

mixer.init()



def stop_playback():
    global is_green,is_stopped, recorded_notes, notes_on,last_note
    is_stopped = True
    is_green = True
    for note in notes_on[:]:  # Use a copy of the list to avoid modification issues during iteration
        sampler.stop(note)
        note_ui.remove_note(note)


    
    notes_on.clear()
    recorded_notes.clear()
    last_note.clear() 
    
    print('Playback stopped and all notes removed from UI')
    recorded_notes = []



def button_stop_callback()-> None:
    global is_recording,is_green,is_stopped
    
    if is_recording:
        is_recording = False
        is_green = True
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recorded_{timestamp}.mid"
        save_midi_file(filename)
        print(f"Recording stopped and MIDI file'{filename}' saved.")
        note_ui.populate_filenames(r'C:\Users\Vyacheslav1911\Desktop\project\songs')
    else:
        stop_playback() 
        print("Not currently recording.")
def save_midi_file(filename)-> None:
    folder_path = r"C:\Users\Vyacheslav1911\Desktop\project\songs"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    full_path = os.path.join(folder_path, filename)
    mid = mido.MidiFile()
    
    track = mido.MidiTrack()
    mid.tracks.append(track)
    tempo = mido.bpm2tempo(120)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo, time= 0))
    ticks_per_beat = 480
    previous_time = 0
    for event in recorded_notes:
        event_type, note_id, velocity, diff_time = event
        delta_time_seconds = diff_time - previous_time
        delta_ticks = int(mido.second2tick(delta_time_seconds, ticks_per_beat, 500000))
        previous_time =  diff_time
        if event_type == 'note_on':
            msg = mido.Message('note_on', note = note_id, velocity=velocity, time=delta_ticks)
        elif event_type == 'note_off':
            msg = mido.Message('note_off', note = note_id, velocity =velocity, time =  delta_ticks)
        track.append(msg)
    mid.save(full_path)
    print(f"MIDI file '{full_path}' has been saved.")


def button_record_callback()-> None:
    global start_time,is_green, is_recording, recorded_notes
    is_green = False
    if is_recording:
        is_recording = False
        
        print("Recording stopped")
        is_green = True
    else:
        is_recording = True
        recorded_notes = []
        start_time = time.time()
        print("Recording started")
def combo_select(event=None):
    selected_value = note_ui.combo.get()  # Get the selected value from the Combobox
    print(f"Selected file: {selected_value}")
    return selected_value
    
def play_recorded_notes():
    global recorded_notes, is_green, is_stopped
    is_stopped = False
    if len(recorded_notes) == 0:
        print("No notes to play")
        return
    is_green = False
    event_index = 0
    start_time = time.time()
    total_events = len(recorded_notes)
    def process_next_event():
        nonlocal event_index
        if event_index >= total_events or is_stopped:
            stop_playback()
            return  # Stop processing if playback is stopped
        event = recorded_notes[event_index]
        event_type, note_id, velocity, event_time = event
        current_time = time.time()
        delay = event_time - (current_time - start_time)

        if delay <= 0:
            # Process the event immediately
            play_and_display(event_type, note_id, velocity)
            event_index += 1
            if not is_stopped:  # Check if playback is still ongoing
                 # Schedule the next event
                note_ui.window.after(0, process_next_event)
           
            
        else:
            # Schedule to process the event after 'delay' milliseconds
            delay_ms = int(delay * 1000)
            if not is_stopped:  # Check stop flag before scheduling
                note_ui.window.after(delay_ms, process_next_event)

    # Start processing events
    process_next_event()



        
    
def button_replay_callback()-> None:

    global is_recording,recorded_notes,start_time
    is_recording = False
    is_green = False
    selected_file = note_ui.combo.get()
    if selected_file:  # Ensure that a file is selected
        file_path = os.path.join(r'C:\Users\Vyacheslav1911\Desktop\project\songs', selected_file)
    try:
        recorded_notes = midi_to_tuple_list(file_path)
    except UnboundLocalError:
        print("Choose the file")
    if len(recorded_notes) > 0:
         print("playing notes", recorded_notes)
         play_recorded_notes() 
             
    else:
        print("no notes loshara")
def play_and_display(event_type, note_id, velocity):
    global last_note
    
    print(f"Playing {event_type} with note {note_id} and velocity {velocity}")
    if event_type == 'note_on':
        sampler.play(note_id, velocity)
        notes_on.append(note_id)
        note_ui.add_note(note_id, is_green)
        last_note.append(note_id)
    elif event_type == 'note_off':
        if note_id in notes_on:
            sampler.stop(note_id)
            notes_on.remove(note_id)
            note_ui.remove_note(note_id)
            print(1)
def midi_to_tuple_list(file_path):
    # Open the MIDI file
    midi = mido.MidiFile(file_path)
    recorded_notes = []
    current_time = 0

    # Iterate over the messages and collect note events
    for msg in midi:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity == 0:
            event_type = 'note_off' 
        else:
            event_type = msg.type
            #recorded_notes.append((event_type, msg.note, msg.velocity, current_time))
        
        if event_type in ['note_on', 'note_off']:
            recorded_notes.append((event_type, msg.note, msg.velocity, current_time))

    return recorded_notes

note_ui = NoteDisplay(button_record_callback, button_replay_callback, button_stop_callback, combo_select)

def note_handler(note: mido.Message)-> None:
    global start_time,is_green, is_recording, recorded_notes

    note_id = int(note.note)
    if note.type == "note_on" and note.velocity >0:
        sampler.play(note_id, note.velocity)
        if note_id not in notes_on:
            notes_on.append(note_id)
        note_ui.add_note(note_id, is_green)
        if is_recording:
                current_time = time.time()
                if start_time:
                    diff_time = current_time - start_time
                    recorded_notes.append(('note_on',note_id, note.velocity, diff_time))
                    
                    

                    
                else:
                    recorded_notes.append(('note_on',note_id, note.velocity, 0))
    elif note.type == 'note_off' or note.type =='note_on' and note.velocity == 0:
       
        notes_on.remove(note_id)
        sampler.stop(note_id)
        note_ui.remove_note(note_id)
        if is_recording:
            current_time = time.time()
            diff_time = current_time - start_time
            recorded_notes.append(('note_off', note_id,note.velocity, diff_time))
        
            
        

        

        
try:
    
    sampler = Sampler(mixer)
    print(mido.get_input_names())
    portname = "LPK25 mk2 0"  # replace with your MIDI INPUT
    with mido.open_input(portname, callback=note_handler) as port:
        print("Using {}".format(port))
        note_ui.window.mainloop()
except Exception as e:
    print(e)