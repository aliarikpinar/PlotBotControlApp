import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import ezdxf
import ezdxf
import matplotlib.pyplot as plt
from CTkMessagebox import CTkMessagebox
import rospy
#from std_msgs.msg import Float32MultiArray
# window 


def browseFiles():
	global filepath
	global save_path
	filename = filedialog.askopenfilename(initialdir = "/",title = "Select your .dxf drawing ",filetypes = ((".DXF files","*.DXF*"),("all files","*.*")))  


	filepath = os.path.relpath(filename)
	print(filepath)
	save_path = filepath + '.png' 
	dxf_file = filepath
	doc = ezdxf.readfile(dxf_file)
	msp = doc.modelspace()

	# Initialize the bounding box coordinates
	min_x = min_y = float('inf')
	max_x = max_y = float('-inf')

	# Iterate over all entities in the modelspace
	for entity in msp:
		if entity.dxftype() == 'LINE':
			start = entity.dxf.start
			end = entity.dxf.end
			min_x = min(min_x, start[0], end[0])
			min_y = min(min_y, start[1], end[1])
			max_x = max(max_x, start[0], end[0])
			max_y = max(max_y, start[1], end[1])

	# Create a figure and axis
	fig, ax = plt.subplots()

	# Iterate over the entities and plot them
	for entity in msp:
		if entity.dxftype() == 'LINE':
			start = entity.dxf.start
			end = entity.dxf.end
			ax.plot([start[0], end[0]], [start[1], end[1]], 'k-')

	# Set the limits of the plot to match the bounding box
	ax.set_xlim(min_x, max_x)
	ax.set_ylim(min_y, max_y)

	# Set the aspect ratio to 'equal' for proper scaling
	ax.set_aspect('equal')
	#plt.show()
	# Save the plot as a PNG image
	fig.savefig(save_path)
	return save_path

def Published_info_message():
    CTkMessagebox(message="Successfully published to ROS",icon="check", option_1="Thanks")
    

def SendDraw(filepath):
	global LinesWillBePublish
	import ezdxf
	
	dxf_file = filepath

	doc = ezdxf.readfile(dxf_file)
	msp = doc.modelspace()
	#print(msp)
	coordinates = []  # Koordinatları depolamak için boş bir dizi

	# Iterate over the entities in the modelspace
	for entity in msp:
		if entity.dxftype() == 'LINE':  # Sadece çizgi tiplerini kontrol etmek isterseniz
			start = entity.dxf.start
			end = entity.dxf.end
			#print(start)
			#print(end)
			coordinates.append(start[0])  # Başlangıç x koordinatını diziye ekle
			coordinates.append(start[1])  # Başlangıç y koordinatını diziye ekle
			coordinates.append(end[0])  # Bitiş x koordinatını diziye ekle
			coordinates.append(end[1])  # Bitiş y koordinatını diziye ekle



	# DXF dosyanızın yolunu belirtin

	LinesWillBePublish = []
	Lines = '\n\n'
	# Koordinatları al
	coordinate_array = coordinates
	#print(coordinate_array)
	# Koordinatları bastır
	for i in range(0, len(coordinate_array), 4):
		start_x = coordinate_array[i]
		start_y = coordinate_array[i+1]
		end_x = coordinate_array[i+2]
		end_y = coordinate_array[i+3]
		#print(f"Çizgi {i//4+1}: Başlangıç: ({start_x}, {start_y}), Bitiş: ({end_x}, {end_y})")
		Lines = Lines + f"Çizgi {i//4+1}: Başlangıç: ({start_x}, {start_y}), Bitiş: ({end_x}, {end_y})" + "\n"
		LinesWillBePublish.append(start_x) 
		LinesWillBePublish.append(start_y) 
		
	print(LinesWillBePublish)
	
	
	#print(Lines)
	Open_Line_Check_Window(Lines)


def PublishToRos(LinesWillBePublish):


	rospy.init_node('publisher_node', anonymous=True)
	pub = rospy.Publisher('array_topic', Float32MultiArray, queue_size=10)
	rate = rospy.Rate(10)  # Yayın hızı (Hz)

	# x adet length'i 2 olan array'i oluşturun
	x = 3
	arrays = LinesWillBePublish  # Örnek olarak üç array

	while not rospy.is_shutdown():
		for array in arrays:
			array_msg = Float32MultiArray()
			array_msg.data = array
			pub.publish(array_msg)
			rate.sleep()

	Published_info_message()
	

	# Save the DXF image as a PNG


    # Change label contents

def Open_Line_Check_Window(Lines):
    new_window = ctk.CTk()
    new_window.title("Check Your Path")
    new_window.geometry("500x650")
    text = Lines
    print(Lines)
    label = ctk.CTkLabel(new_window, text = Lines, corner_radius = 2,textvariable = string_var,font =("Arial", 18),)
    label.place(x=10,y=10)
    PublishButton =ctk.CTkButton(
	master=new_window,
 	text="PUBLISH TO ROS",
	
	width=100,
	height=70,
	 #compound="left",
 	fg_color='#FFFFF0',
  text_color="#0A0A0A",
  font=("Arial",18),
	hover_color='#303030',
 command=PublishToRos(LinesWillBePublish)).place(x=150,y=518)
    new_window.mainloop()

window = ctk.CTk()
window.title('PlotBot Control Software')
window.geometry('1355x800')


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# widgets 
string_var = ctk.StringVar(value = 'Control The PlotBot')
label = ctk.CTkLabel(
	window, 
	text = 'Control The PlotBot', 
	#fg = ('blue','red'), 
	#color = ('black','white'),
	corner_radius = 2,
	textvariable = string_var,
 	font =("Arial", 25))
label.place(x=140,y=100)




string_var = ctk.StringVar(value = 'PlotBot Status')
label = ctk.CTkLabel(
	window, 
	text = 'PlotBot Status', 
	#fg = ('blue','red'), 
	#color = ('black','white'),
	corner_radius = 2,
	textvariable = string_var,
 	font =("Arial", 25))
label.place(x=1060,y=100)

string_var = ctk.StringVar(value = 'Drawing Selection')
label = ctk.CTkLabel(
	window, 
	#text = 'PlotBot Status', 
	#fg = ('blue','red'), 
	#color = ('black','white'),
	corner_radius = 2,
	textvariable = string_var,
 	font =("Arial", 25))
label.place(x=610,y=100)


string_var = ctk.StringVar(value = '     Connected    ')
label = ctk.CTkLabel( 
	window, 

	#text = 'PlotBot Status', 
	fg_color = ('blue','green'), 
	text_color = ('black','white'),
	corner_radius = 6,
	textvariable = string_var,
 	font =("Arial", 30))
label.place(x=1030,y=150)
print(dir(ctk.CTkLabel(window)))

string_var = ctk.StringVar(value = 'Drawing Sended')
label = ctk.CTkLabel(
	window, 

	#text = 'PlotBot Status', 
	fg_color = ('blue','white'), 
	text_color = ('black','black'),
	corner_radius = 6,
	textvariable = string_var,
 	font =("Arial", 30))
label.place(x=1030,y=200)


string_var = ctk.StringVar(value = '    In Progress    ')
label = ctk.CTkLabel(
	window, 

	#text = 'PlotBot Status', 
	fg_color = ('blue','white'), 
	text_color = ('black','black'),
	corner_radius = 6,
	textvariable = string_var,
 	font =("Arial", 30))
label.place(x=1030,y=250)

string_var = ctk.StringVar(value = '    Completed     ')
label = ctk.CTkLabel(
	window, 

	#text = 'PlotBot Status', 
	fg_color = ('blue','white'), 
	text_color = ('black','black'),
	corner_radius = 6,
	textvariable = string_var,
 	font =("Arial", 30))
label.place(x=1030,y=300)
print(dir(ctk.CTkLabel(window)))

def buton1():
	pass


def select(event):
	global imgHopstıch
	global imgFootballPitch

	if event == "Hopstoch":
		img23 = ImageTk.PhotoImage(Image.open("libs\images\Hopstoch.jpg").resize((400,400),Image.ANTIALIAS)),
		labela.configure(image=img23)
	if event == "Football Pitch":
		img23 = ImageTk.PhotoImage(Image.open("libs\images\FootballPitch.jpg").resize((400,400),Image.ANTIALIAS)),
		labela.configure(image=img23)
	
	

	if event == "DXF Drawing":
		print(save_path)
		img23 = ImageTk.PhotoImage(Image.open(save_path).resize((400,400),Image.ANTIALIAS)),
		labela.configure(image=img23)
	
Drop = ctk.CTkOptionMenu(window,command=select,	values=["Hopstoch","Football Pitch","DXF Drawing"],
    width=440,
    font=("arial",25),
    height=70).place(x=500,y=150)


img = ImageTk.PhotoImage(Image.open(r"libs/images/Hopstoch.jpg"),Image.ANTIALIAS)

labela = ctk.CTkLabel(
    
	window, 
 text="",
	image=img,
	#bg_color=("white"),
	#text = 'PlotBot Status', 
	fg_color = ('white','white'), 
	text_color = ('white'),
	corner_radius = 10,
 width=440,
 height=390
	#textvariable = string_var,
 	#font =("Arial", 30))
)
labela.place(x=500,y=240)



    #label_file_explorer.configure(text="File Opened: "+filename)

SendOpretionButton = ctk.CTkButton(
	master=window,
 	text="SEND DRAW",
	
	width=440,
	height=102,
	 #compound="left",
 	fg_color='#FFFFF0',
  text_color="#0A0A0A",
  font=("Arial",36),
	hover_color='#303030',
 command=lambda:SendDraw(filepath)).place(x=500,y=650)

ForwardArrayImage = ImageTk.PhotoImage(Image.open(r"libs/images/FowardArray.png").resize((100,100),Image.ANTIALIAS))
ForwardButton = ctk.CTkButton(
	master=window,
 	text="",
	image=ForwardArrayImage,
	width=102,
	height=102,
	 #compound="left",
 	fg_color='#000',
	hover_color='#303030',
 command=buton1).place(x=190,y=150)

BackwardArrayImage = ImageTk.PhotoImage(Image.open(r"libs/images/BackwardArray.png").resize((100,100),Image.ANTIALIAS))
BackwardButton = ctk.CTkButton(
	master=window,
 	text="",
	image=BackwardArrayImage,
	width=102,
	height=102,
	 #compound="left",
 	fg_color='#000',
	hover_color='#303030',
 command=buton1).place(x=190,y=270)

LeftArrayImage = ImageTk.PhotoImage(Image.open(r"libs/images/LeftArray.png").resize((100,100),Image.ANTIALIAS))
BackwardButton = ctk.CTkButton(
	master=window,
 	text="",
	image=LeftArrayImage,
	width=102,
	height=102,
	 #compound="left",
 	fg_color='#000',
	hover_color='#303030',
 command=buton1).place(x=70,y=270)


RightArrayImage = ImageTk.PhotoImage(Image.open(r"libs/images/RightArray.png").resize((100,100),Image.ANTIALIAS))
BackwardButton = ctk.CTkButton(
	master=window,
 	text="",
	image=RightArrayImage,
	width=102,
	height=102,
	 #compound="left",
 	fg_color='#000',
	hover_color='#303030',
 command=buton1).place(x=310,y=270)








ImportDXFButton = ctk.CTkButton(
	master=window,
 	text="Import DFX",
	
	width=302,
	height=102,
	 #compound="left",
 	fg_color='#FFFFF0',
  text_color="#0A0A0A",
  font=("Arial",36),
	hover_color='#303030',
 command=lambda: browseFiles()).place(x=995,y=370)


StartOpretionButton = ctk.CTkButton(
	master=window,
 	text="START",
	
	width=352,
	height=102,
	 #compound="left",
 	fg_color='#FFFFF0',
  text_color="#0A0A0A",
  font=("Arial",36),
	hover_color='#303030',
 command=buton1).place(x=70,y=400)

StopOpretionButton = ctk.CTkButton(
	master=window,
 	text="STOP",
	
	width=352,
	height=102,
	 #compound="left",
 	fg_color='#FFFFF0',
  text_color="#0A0A0A",
  font=("Arial",36),
	hover_color='#303030',
 command=buton1).place(x=70,y=530)





    
# run
window.mainloop()