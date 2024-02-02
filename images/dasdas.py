import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import ezdxf
import ezdxf    
new_window = ctk.CTk()
new_window.title("Check Your Path")
new_window.geometry("900x900")
Lines = "dsasdaddasd"
text = Lines
print(Lines)
label = ctk.CTkLabel(window, text = Lines, corner_radius = 2,textvariable = string_var,font =("Arial", 9))
label.place(x=10,y=10)
label = ctk.CTkLabel(
    window, 
    text = 'Control The PlotBot', 
    fg = ('blue','red'), 
    color = ('black','white'),
    corner_radius = 2,
    textvariable = string_var,
    font =("Arial", 25))
label.place(x=140,y=100)
new_window.mainloop()