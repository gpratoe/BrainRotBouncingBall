from pygame import mixer
import pygame

class Sounds:
    def __init__(self):
        mixer.init()
        self.sounds = {"c6": mixer.Sound("sounds/c6.mp3"),
                       "d6": mixer.Sound("sounds/d6.mp3"),
                       "e6": mixer.Sound("sounds/e6.mp3"),
                       "f6": mixer.Sound("sounds/f6.mp3"),
                       "g6": mixer.Sound("sounds/g6.mp3"),
                       "a6": mixer.Sound("sounds/a6.mp3")}
        
        self.song = ["c6", "c6", "d6", "c6", "f6", "e6",
                     "c6", "c6", "d6", "c6", "g6", "f6",
                     "c6", "c6", "a6", "f6",
                     "f6", "f6", "e6", "d6",
                     "a6", "a6", "g6", "e6", "g6", "f6"]
        
        self.next_note = 0
        

    def play(self):
        # for sound in self.sounds.values(): # suena mejor si no se corta el sonido anterior
        #     sound.stop()
        
        note = self.sounds[self.song[self.next_note]]
        print("Playing note: ", self.song[self.next_note])
        self.next_note = (self.next_note + 1) % self.song.__len__()
        note.play()
        
