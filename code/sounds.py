from pygame import mixer
from random import randint as ri

class Sounds:
    def __init__(self):
        mixer.pre_init(44100,16,2,4096)
        mixer.init()

        self.sounds = {"single": None,
                       "composite": [],
                       "notes":{}
                        }

        notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        for i in range (5, 7):
            for note in notes:
                self.sounds["notes"][note + str(i)] = mixer.Sound("sounds/notes/vibraphone/" + note + str(i) + ".wav")
        self.sounds["notes"]["C7"] = mixer.Sound("sounds/notes/vibraphone/C7.wav")


        for i in range(1, 12):
            self.sounds["composite"].append(mixer.Sound("sounds/pingpongdeluxe-" + str(i) + ".wav"))

        self.song = ["C6", "C7", "B6", "G6", "A6", "B6",
                     "C7", "C6", "A6", "G6", "A5", "F6", 
                     "E6", "C6", "D6", "E6", "F6", "D6", 
                     "B5", "C6", "D6", "E6", "C6"]
        
        self.next_note = 0
        self.next_note_comp = 0

    def play_song(self):
        for sound in self.sounds["notes"].values():
            sound.stop()
        
        self.sounds["notes"][self.song[self.next_note]].play()
        self.next_note = (self.next_note + 1) % len(self.song)
        


    def play_composite(self):
        for sound in self.sounds["composite"]:
            sound.stop()

        self.sounds["composite"][self.next_note_comp].play()
        self.next_note_comp = (self.next_note_comp + 1) % len(self.sounds["composite"])

    def set_sound(self, sound_path):
        self.sounds["single"] = mixer.Sound(sound_path)
    
    def play_single_sound(self):
        self.sounds["single"].stop()
        self.sounds["single"].play()    
        
