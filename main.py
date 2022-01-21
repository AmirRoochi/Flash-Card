import tkinter
from tkinter import *
import pandas as pd
import csv
from tkinter import messagebox
import random
import pyperclip
import json
import os

BACKGROUND_COLOR = "#B1DDC6"
try:
    df = pd.read_csv("data/to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("data/english_words.csv")
data_dict = df.to_dict(orient="records")
current_card = {}
is_front = True


# -------------------------------------pick word--------------------------------#
def pick_random():
    global current_card
    global is_front
    random_word = random.choice(data_dict)
    current_card = random_word
    canvas.itemconfig(canvas_image, image=front_image)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=random_word["english"])
    is_front = False

# -------------------------------------create known list----------------------#
def known_word():
    global data_dict
    try:
        global current_card
        data_dict.remove(current_card)
        new_data = pd.DataFrame(data_dict)
        new_data.to_csv('./data/to_learn.csv', index=False)
        pick_random()
    except ValueError:
        messagebox.showinfo(title="Congratulations", message="You know all the words. To start over restart the app.")
        os.remove("data/to_learn.csv")
    except IndexError:
        messagebox.showinfo(title="Congratulations", message="You know all the words. To start over restart the app.")
        os.remove("data/to_learn.csv")
# -------------------------------------Flip Card-------------------------#

def flip_card():
    global current_card
    global is_front
    farsi_word = ""
    if is_front:
        canvas.itemconfig(canvas_image, image=front_image)
        canvas.itemconfig(card_title, text="English")
        canvas.itemconfig(card_word, text=current_card["english"])
        is_front = False
    else:
        if " " in current_card["farsi"]:
            words = current_card["farsi"].split(" ")
            farsi_word = " ".join(reversed(words))
        else:
            farsi_word = current_card["farsi"]
        canvas.itemconfig(canvas_image, image=back_image)
        canvas.itemconfig(card_title, text="فارسی")
        canvas.itemconfig(card_word, text=farsi_word)
        is_front = True


# -------------------------------------UI--------------------------------#
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(widt=820, height=535, bg=BACKGROUND_COLOR)
canvas.config(highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
front_image = PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(410, 268, image=front_image, anchor=CENTER)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 270, text="", font=("Arial", 60, "bold"))

back_image = PhotoImage(file="./images/card_back.png")

cross_image = PhotoImage(file="./images/wrong.png")
cross_button = Button(image=cross_image, highlightthickness=0, command=pick_random)
cross_button.grid(column=0, row=2)

thick_image = PhotoImage(file="./images/right.png")
thick_button = Button(image=thick_image, highlightthickness=0, command=known_word)
thick_button.grid(column=1, row=2)

flip_image = PhotoImage(file="./images/flip_button.png")
flip_button = Button(image=flip_image, highlightthickness=0, command=flip_card)
flip_button.grid(column=3, row=0)


pick_random()
window.mainloop()




