"""
from SER_helpers import convert_audio, labels
from keras.models import load_model
from keras import optimizers
from keras.utils import np_utils
"""
import tkinter as tk
from tkinter import LabelFrame, StringVar, Label, Button
import os
import numpy as np
import pandas as pd
import glob

def record():
    pass

def import_audio():
    pass

app = tk.Tk()
wrapper = LabelFrame(app, text="Speech Emotion Recogniser")
wrapper.pack(fill="both", expand="yes", padx=10, pady=10)

file_var = StringVar()
activity_var = StringVar()

file_var.set("No file imported")
activity_var.set("No activity detected")

file_lbl = Label(wrapper, textvariable=file_var)
activity_lbl = Label(wrapper, textvariable=activity_var)

file_lbl.grid(row=0, column=0, padx=(10, 20))
activity_lbl.grid(row=0, column=1, padx=(10, 20))

import_btn = Button(wrapper, text="Import audio", command=import_audio)
import_btn.grid(row=1, column=0, padx=(10, 20))
record_btn = Button(wrapper, text="Start recording", command=record)
record_btn.grid(row=1, column=1, padx=(10, 20))

app.title("SER - Daniel Jones")
app.geometry("800x450")
app.mainloop()


"""
PATH2 = "me_tests/me_sad.wav"
x = convert_audio(PATH2)

model = load_model("model/SER_Model_2DCNN.h5")
model.load_weights("model/SER_Model_2DCNN.h5")
opt = optimizers.Adam(learning_rate=0.0001, beta_1=0.9,  beta_2=0.999, amsgrad=False)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

predictions = model.predict(np.array([x]))[0]

for c, i in enumerate(predictions):
    print(("%.17f" % i).rstrip('0').rstrip('.'), labels[c])
"""