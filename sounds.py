from pygame import mixer
import pygame
from random import randint as ri

class Sounds:
    def __init__(self):
        mixer.init()
        self.sounds = {"single": None,
                       "c6": mixer.Sound("sounds/c6.mp3"),
                       "d6": mixer.Sound("sounds/d6.mp3"),
                       "e6": mixer.Sound("sounds/e6.mp3"),
                       "f6": mixer.Sound("sounds/f6.mp3"),
                       "g6": mixer.Sound("sounds/g6.mp3"),
                       "a6": mixer.Sound("sounds/a6.mp3")}
        
        self.pong = []
        for i in range(1, 12):
            self.pong.append(mixer.Sound("sounds/pingpongdeluxe-" + str(i) + ".wav"))

        self.song = ["c6", "c6", "d6", "c6", "f6", "e6",
                     "c6", "c6", "d6", "c6", "g6", "f6",
                     "c6", "c6", "a6", "f6",
                     "f6", "f6", "e6", "d6",
                     "a6", "a6", "g6", "e6", "g6", "f6"]
        
        self.next_note = 0

    def play_song(self):
        for sound in self.sounds.values():
            sound.stop()
        
        note = self.sounds[self.song[self.next_note]]
        self.next_note = (self.next_note + 1) % self.song.__len__()
        note.play()

    def play_pong(self):
        for sound in self.pong:
            sound.stop()

        self.pong[ri(0,self.pong.__len__()-1)].play()
        


    def set_sound(self, sound_path):
        self.sounds["single"] = mixer.Sound(sound_path)
    
    def play_single_sound(self):
        self.sounds["single"].stop()
        self.sounds["single"].set_volume(ri(70, 100)/100)
        self.sounds["single"].play()    
        
