import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), '..'))

import sounddevice as sd
import queue
import vosk
import json
import datetime as dt
from config import DEBUG


SAMPLE_RATE = 32000
DEVICE_ID = 1

#Время отведенное на распознавание команды в секундах
TIMEOUT = 8

#Скорость распознавания речи. Чем менее цифра - тем быстрее, но более прожорливее по цпу
BLOCKSIZE = 16000


class VoiceRecognition:
    def __init__(self):
        self.model = vosk.Model("voice_module/vosk-model")

        self.q = queue.Queue()

    def __callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def wait_call(self):
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCKSIZE, device=DEVICE_ID, dtype='int16',
                               channels=1, callback=self.__callback):
            self.rec = vosk.KaldiRecognizer(self.model, SAMPLE_RATE)
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    self.rec.Result()
                else:
                    partial = json.loads(self.rec.PartialResult())['partial']
                    if len(partial.split(" ")) > 10:
                        partial = ""
                        self.rec.Reset()
                    if partial != "" and DEBUG: print("[VOICE_REC] INPUT: " + partial)
                    with open("voice_module/calls.json", encoding='utf8') as calls:
                        calls_dict = json.loads(calls.read())
                        for call in calls_dict["calls"]:
                            if call in partial:
                                if DEBUG: print("[VOICE_REC] CALL FOUND " + call)
                                return True

    def wait_command(self):
        start_time = dt.datetime.now()
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCKSIZE, device=DEVICE_ID, dtype='int16',
                               channels=1, callback=self.__callback):
            self.rec = vosk.KaldiRecognizer(self.model, SAMPLE_RATE)
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())['text']
                    if result != "":
                        return result
                else:
                    partial = json.loads(self.rec.PartialResult())['partial']
                    if DEBUG and partial != "": print(f"[VOICE_REC] INPUT at ({dt.datetime.time(dt.datetime.now())}): {partial}")
                    if dt.datetime.now() - dt.timedelta(seconds=TIMEOUT) > start_time and partial == "":
                        return None

    def start_recognition(self):
        while True:
            if self.wait_call():
                print("Распознавание речи...", end=" ")
                command =  self.wait_command()
                if command != "не удалось распознать речь":
                    return command
                print("не удалось распознать речь")

if __name__ == "__main__":
    voice_rec = VoiceRecognition()
    voice_rec.start_recognition()
