from tkinter import *
import os
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1913

IMAGE_NAMES = [
    "key_green_left",
    "key_green_mid",
    "key_green_right",
    "key_green_top",
    "key_red_left",
    "key_red_mid",
    "key_red_right",
    "key_red_top",
]
NOTES_TO_IMAGE_MAP = {
    0: "left",
    1: "top",
    2: "mid",
    3: "top",
    4: "right",
    5: "left",
    6: "top",
    7: "mid",
    8: "top",
    9: "mid",
    10: "top",
    11: "right",
    12: "left",
}
NOTES_Y = 612
NOTES_X = {
    13: -150,
    26: -170,
    27: -170,
    28: -170,
    29: -170,
    30: -170,
    21: -170,
    31: -170,
    32: -100,  # Example position
    33: -50,
    34: 0,
    35: -180,
    36: 3,
    37: 42,
    38: 56,
    39: 97, 
    40: 113,#e
    41: 168,
    42: 207,
    43: 222,
    44: 262,
    45: 277,
    46: 317,
    47: 332,
    48: 387,
    49: 426,
    50: 442,
    51: 481,
    52: 497,
    53: 552,
    54: 591,
    55: 607,
    56: 646,
    57: 662,
    58: 701,
    59: 717,
    60: 772,
    61: 811,
    62: 827,
    63: 866,
    64: 882,
    65: 937,
    66: 976,
    67: 991,
    68: 1031,
    69: 1046,
    70: 1086,
    71: 1101,
    72: 1156,
    73: 1196,
    74: 1211,
    75: 1251,
    76: 1266,
    77: 1321,
    78: 1361,
    79: 1375,
    80: 1415,
    81: 1431,
    82: 1470,
    83: 1486,
    84: 1541,
    85: 1950,
    86: 1960,
    87: 1980,
    88: -140,
    89: -180,
    90: -180,
    91: -180
}

class NoteDisplay():
    def __init__(self, button_record_callback, button_replay_callback,button_stop_callback,combo_select):
        self.window = Tk()
        self.window.title("Project000")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.frame = Frame(self.window)
        self.frame.pack(side=RIGHT)
        self.canvas = Canvas(self.frame, width = WINDOW_WIDTH , height=WINDOW_HEIGHT )
        self.canvas.pack()

        self.keys_img = ImageTk.PhotoImage(Image.open("images/keys1.png"))
        self.canvas.create_image(0, 611, image = self.keys_img, anchor = 'w')
        self.images = {}
        
        self.notes_widgets = {}
        for i in IMAGE_NAMES:
            image = ImageTk.PhotoImage(Image.open(f"images/{i}.png"))
            self.images[i] = image
        self.filenames = []
        self.combo_var = StringVar()
        
        self.combo = Combobox(self.canvas, values=self.filenames )
        self.combo.bind("<<ComboboxSelected>>", combo_select)
        self.combo.pack()
        self.button_replay = Button(self.canvas, text= "Replay", command = button_replay_callback, height = 2, width = 20 )
        self.button_record = Button(self.canvas, text= "Record", command = button_record_callback, height = 2, width = 20 )
        self.button_stop= Button(self.canvas, text= "Stop", command = button_stop_callback, height = 2, width = 20 )
        self.canvas.create_window(300,100, window = self.button_record)
        self.canvas.create_window(450,100, window = self.button_stop)
        self.canvas.create_window(300,200, window = self.button_replay)
        self.canvas.create_window(500,200, window = self.combo)
        self.populate_filenames(r'C:\Users\Vyacheslav1911\Desktop\project\songs') 
    def populate_filenames(self, folder_path):
        self.filenames.clear()
        for filename in os.listdir(folder_path):
            if filename.endswith('.mid'):  # Ensure only MIDI files are listed
                self.filenames.append(filename)
        print("Updated filenames:", self.filenames)
        self.combo['values'] = self.filenames
        self.combo_var.set('')  # Reset the selection
        self.combo.update_idletasks()  # Refresh the Combobox

        

    def get_note_image(self, note_id: int) -> None:
        """
        Get a note`s image
        """
        real_note = None
        for n in [84, 72, 60, 48, 36, 24, 12]:
            if note_id >= n:
                real_note = note_id - n
                break
        return NOTES_TO_IMAGE_MAP[real_note] if real_note is not None else None
    def add_note(self, note_id = int, is_green: bool= True):
        note_name = self.get_note_image(note_id)
        if note_name is None:
            print(f"Note name for note_id {note_id} is None.")
            return
        if is_green:
            note_image_name = f"key_green_{note_name}" 
        else:
            note_image_name = f"key_red_{note_name}"
        new_img = self.canvas.create_image(NOTES_X[note_id], NOTES_Y, image = self.images[note_image_name], anchor = "w")
        if note_id not in self.notes_widgets:
            self.notes_widgets[note_id] = []
        #check
        self.notes_widgets[note_id].append(new_img)
    def remove_note(self, note_id: int) -> None:
        if note_id in self.notes_widgets and self.notes_widgets[note_id]:
            while self.notes_widgets[note_id]:
                img_id = self.notes_widgets[note_id].pop()
                self.canvas.delete(img_id)
            if not self.notes_widgets[note_id]:
                self.canvas.delete(self.notes_widgets[note_id])
            
                
        else:
            print(f"Warning: Note {note_id} not found in notes_widgets during remove_note.")





if __name__ == "__main__":
    app = NoteDisplay()