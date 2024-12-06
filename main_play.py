from pygame import mixer

class Sampler:
    def __init__(self, mix:mixer):
        mix.set_num_channels(32)
        self.id_to_note = {}
        self.id_to_file = {}
        notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        octave = 1
        notes_id = 0
        for i in range(24, 96):
            self.id_to_note[i] = f"{notes[notes_id]}"
            self.id_to_file[i] = f"Piano.ff.{notes[notes_id]}{octave}.aiff"
            notes_id +=1
            if notes_id == len(notes):
                octave += 1
                notes_id = 0
            self.sounds = {}
            for id, name in self.id_to_file.items():
                self.sounds[id] = mix.Sound("samples/"+name)
    def play(self,note_id: int, vel: int )-> None:
        self.sounds[note_id].stop()
        self.sounds[note_id].set_volume(float(vel/127) * 1.0)
        self.sounds[note_id].play()
    def stop(self, note_id: int)-> None:
        self.sounds[note_id].fadeout(400)



