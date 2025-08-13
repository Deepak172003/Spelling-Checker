import tkinter as tk
from tkinter import messagebox, filedialog
from textblob import TextBlob
import pyttsx3
import language_tool_python

# Initialize main window
root = tk.Tk()
root.title("Spelling & Grammar Checker")
root.geometry("700x600")
root.configure(bg="#dae6f6")

# Initialize text-to-speech engine & grammar tool
engine = pyttsx3.init()
tool = language_tool_python.LanguageTool('en-US')

# Variable to store corrected text
corrected_text_var = tk.StringVar()

def check_text():
    text = text_input.get("1.0", "end-1c").strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    # Fix spelling first
    corrected_text = str(TextBlob(text).correct())
    
    # Fix grammar
    corrected_text = language_tool_python.utils.correct(corrected_text, tool.check(corrected_text))
    
    corrected_text_var.set(corrected_text)

def clear_text():
    text_input.delete("1.0", tk.END)
    corrected_text_var.set("")

def copy_text():
    root.clipboard_clear()
    root.clipboard_append(corrected_text_var.get())
    root.update()
    messagebox.showinfo("Copied", "Text copied to clipboard!")

def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(corrected_text_var.get())
        messagebox.showinfo("Saved", "File saved successfully!")

def read_text():
    text = corrected_text_var.get()
    if text:
        engine.say(text)
        engine.runAndWait()
        messagebox.showinfo("Reading", "Reading aloud completed!")

# UI Components
tk.Label(root, text="Spelling & Grammar Checker", font=("Trebuchet MS", 24, "bold"), bg="#dae6f6", fg="#364971").pack(pady=20)

# Text Input with Scrollbar
text_frame = tk.Frame(root)
text_frame.pack(pady=10)

scrollbar = tk.Scrollbar(text_frame)
text_input = tk.Text(text_frame, height=10, width=50, font=("Poppins", 14), yscrollcommand=scrollbar.set)
scrollbar.config(command=text_input.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_input.pack()

# Buttons
button_frame = tk.Frame(root, bg="#dae6f6")
button_frame.pack(pady=10)

buttons = [
    ("Check", "red", check_text),
    ("Clear", "blue", clear_text),
    ("Copy", "green", copy_text),
    ("Save", "purple", save_text),
    ("Read", "orange", read_text),
]

for text, color, command in buttons:
    tk.Button(button_frame, text=text, font=("Arial", 16, "bold"), fg="white", bg=color, command=command).pack(side=tk.LEFT, padx=8)

# Corrected Text Display
tk.Label(root, text="Corrected Text:", font=("Poppins", 18), bg="#dae6f6", fg="#364971").pack(pady=10)
tk.Label(root, textvariable=corrected_text_var, font=("Poppins", 16), bg="#dae6f6", fg="black", wraplength=600, justify="left").pack()

# Run Application
root.mainloop()
