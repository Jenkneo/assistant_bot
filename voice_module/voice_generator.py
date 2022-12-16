import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), '..'))

import torch
import sounddevice as sd
import time
from config import SPEAKER

LANGUAGE = 'ru'
MODEL_ID = 'ru_v3'
SAMPLE_RATE = 48000
PUT_ACCENT = True
PUT_YO = True
device = torch.device('cpu') #cpu, cuda, xpu, mkldnn, opengl, opencl, ideep, hip, ve, ort, mlc, xla, lazy, vulkan, meta, hpu

class Speaker:
    def __init__(self):
        self.model, _ =  torch.hub.load(repo_or_dir='snakers4/silero-models',
                                   model = 'silero_tts',
                                   language = LANGUAGE,
                                   speaker = MODEL_ID)

        self.model.to(device)

    def say(self, text):
        self.audio = self.model.apply_tts(text = text,
                                speaker = SPEAKER,
                                sample_rate = SAMPLE_RATE,
                                put_accent = PUT_ACCENT,
                                put_yo = PUT_YO)

        sd.play(self.audio, SAMPLE_RATE * 1.05)
        time.sleep((len(self.audio)/SAMPLE_RATE) + 0.5)
        sd.stop()

if __name__ == "__main__":
    spek = Speaker()
    SPEAKER = 'baya'
    text = "Привет, это Байя!"
    spek.say(text);
    print(text)

    SPEAKER = 'kseniya';
    text = "Привет, это Ксения!"
    spek.say(text);
    print(text)

    SPEAKER = 'xenia';
    text = "Привет, это тоже Ксения!"
    spek.say(text);
    print(text)

    SPEAKER = 'aidar';
    text = "Привет, а это я, Айдар!"
    spek.say(text);
    print(text)