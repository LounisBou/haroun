#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#

import subprocess
import sys

from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 16000

# You can set log level to -1 to disable debug messages
SetLogLevel(0)

# Define language model to use.
#model = Model(lang="fr")

# You can also init model by name or with a folder path
model = Model(model_name="vosk-model-fr-0.6-linto-2.2.0")

rec = KaldiRecognizer(model, SAMPLE_RATE)

with subprocess.Popen(
    ["ffmpeg", "-loglevel", "quiet", "-i", sys.argv[1], "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
    stdout=subprocess.PIPE
) as process:

    # Listenning loop.
    while True:

        # Read data.
        data = process.stdout.read(4000)

        # If data is empty.
        if len(data) == 0:
            # Break listenning loop.
            break

        # If data is valid.
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())

    print(rec.FinalResult())
