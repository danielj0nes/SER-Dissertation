"""Daniel Jones - SER GUI"""
# Import libraries
from tkinter import LabelFrame, StringVar, Label, Button, END, Text
from tkinter.filedialog import askopenfilename
import _thread
import tkinter as tk
import numpy as np

from keras.models import load_model
from keras import optimizers
from Voice_Recorder import RecAUD
from SER_helpers import convert_audio, labels

# Load model with standard configuration settings
opt = optimizers.Adam(learning_rate=0.0001, beta_1=0.9,  beta_2=0.999, amsgrad=False)
model = load_model("model/SER_Model_2DCNN.h5")
model.load_weights("model/SER_Model_2DCNN.h5")
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

def predict_emotion(filepath):
    """Convert the audio and use the model to make a prediction"""
    values_box.delete("1.0", END)
    values_box.insert(END, "Loading...")
    converted_audio = convert_audio(filepath)
    predictions = model.predict(np.array([converted_audio]))[0]
    converted = {labels[c]: format(i, '.8f') for c, i in enumerate(predictions)}
    values_box.delete("1.0", END)
    for key, value in sorted(converted.items(), key=lambda item: item[1], reverse=True):
        values_box.insert(END, key + " " + value + "\n")

def load_audio():
    """Open a file to get the file path then predict the emotion"""
    filepath = askopenfilename()
    file_var.set(filepath)
    _thread.start_new_thread(predict_emotion, (filepath,))

def record():
    """Activate the helper function to record some audio, predict emotions once finished"""
    activity_var.set("Recording...")
    predict_emotion(ra.start_record())

def stop_record():
    """End the recording and set the file label to the newly recorded file"""
    activity_var.set("Not recording")
    file_var.set(ra.last_name)
    ra.stop()

# Initialisations
app = tk.Tk()
ra = RecAUD(app)
wrapper = LabelFrame(app, text="Speech Emotion Recogniser")
wrapper.pack(fill="both", expand="yes", padx=10, pady=10)
# Set labels
file_var = StringVar()
activity_var = StringVar()
values_var = StringVar()
file_var.set("No file imported")
activity_var.set("Not recording")
values_var.set("Predictions (in order of most likely)")
file_lbl = Label(wrapper, textvariable=file_var)
activity_lbl = Label(wrapper, textvariable=activity_var)
values_lbl = Label(wrapper, textvariable=values_var)
# Set buttons
file_btn = Button(wrapper, text="Load audio", command=load_audio)
activity_btn = Button(wrapper, text="Start recording", command=record)
stop_btn = Button(wrapper, text="Stop recording", command=stop_record)
# Label positioning
file_lbl.place(x=0, y=0)
activity_lbl.place(x=0, y=130)
values_lbl.place(x=285, y=20)
# Button positioning
file_btn.place(x=0, y=30)
activity_btn.place(x=0, y=160)
stop_btn.place(x=100, y=160)
# Value box positioning
values_box = Text(app, width=40, height=12) # Height = length of predictions
values_box.place(x=300, y=70)
# GUI defaults
app.title("SER - Daniel Jones")
app.geometry("800x450")
app.mainloop()
