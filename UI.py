import tkinter as tk
import pyttsx3
import pyautogui
from twilio.rest import Client
from PIL import Image, ImageTk
import PIL

# Click a spot
def click(x, y):
    pyautogui.click(x, y)

def sendSMS(msg):
    account_sid = 'AC16084c175b97d6028f37ff709da9cd93'
    auth_token = 'a79aed5c60ecf3756310abff0d662192'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=msg,
        from_='+15636075300',
        to='+16476392070'
    )
    print(message.sid)

# Function to speak the button text
def speak_button_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    # sendSMS(text)
    engine.runAndWait()

def click_button(index):
    # Automatically click the button at the specified index
    speak_button_text(button_data[index]["text"])  # Speak the button text
    
    # Change the button color to red
    buttons[index].config(bg="red")
    
    # After 500 milliseconds, change the button color back to its original color
    root.after(500, lambda: buttons[index].config(bg=root.cget('bg')))
    
    buttons[index].invoke()  # Trigger the button click

root = tk.Tk()
root.attributes('-fullscreen', True)

# Define button data: text, image file path
button_data = [
    {"text": "Yes", "image_path": "yes.jpg"},
    {"text": "NO", "image_path": "no.jpg"},
    {"text": "Washroom", "image_path": "washroom.jpg"},
    {"text": "Food", "image_path": "food.png"},
    {"text": "Water", "image_path": "water.jpg"},
    {"text": "Help", "image_path": "help.jpg"}
]

buttons = []
for i, data in enumerate(button_data):
    button_text = data["text"]
    image_path = data["image_path"]

    # Load the image and create a PhotoImage object
    img = Image.open(image_path)
    img = img.resize((100, 100), PIL.Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    button = tk.Button(root, text=button_text, image=img, compound=tk.TOP, padx=20, pady=10, font=("Helvetica", 20))
    button.image = img  # Keep a reference to the image to prevent it from being garbage collected

    row = i // 2
    col = i % 2
    button.grid(row=row, column=col, sticky="nsew")
    buttons.append(button)
    button.bind("<Button-1>", lambda event, text=button_text: speak_button_text(text))

# Bind key presses for each button (0-5)
for i in range(len(buttons)):
    root.bind(str(i), lambda event, index=i: click_button(index))

for i in range(2):
    root.grid_rowconfigure(i, weight=1)
for i in range(2):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
