import customtkinter as ctk
from tkinter import messagebox
import tkintermapview
from CTkListbox import *
from PIL import Image

window = ctk.CTk()
window.geometry('1200x700')
window.title('Map')
window.iconbitmap('map.ico')
window.minsize(width=864, height=504)
ctk.set_appearance_mode("light")

my_font = ('Arial', 18)

map_view_image = ctk.CTkImage(light_image=Image.open('map.png'), size=(20, 20))
terrain_view_image = ctk.CTkImage(light_image=Image.open('terrain.png'), size=(20, 20))
google_view_image = ctk.CTkImage(light_image=Image.open('google_map_image.png'), size=(20, 20))

map_widget = tkintermapview.TkinterMapView(window, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.6, rely=0.5, anchor=ctk.CENTER, relwidth=0.8, relheight=1)
map_widget.set_position(52.661110, -8.575090)
map_widget.set_zoom(17)

def take_to_address(event):
    try:
        address = address_entry.get()
        full_address = map_widget.set_address(address, marker=True)
        history_frame.insert('END', full_address.text)
        history_frame.update_idletasks()
    except:
        messagebox.showerror('Error', 'Invalid Location')

def return_to_previous_location(event):
    selected_index = history_frame.curselection()
    selected_item = history_frame.get(selected_index)
    coords = tkintermapview.convert_address_to_coordinates(selected_item)
    map_widget.set_position(coords[0], coords[1])
    map_widget.set_zoom(17)

address_entry = ctk.CTkEntry(window, corner_radius=0, width=180)
address_entry.place(relx=0.5, rely=0.95)

class HistoryFrame(CTkListbox):
    def __init__(self, parent):
        super(HistoryFrame, self).__init__(master=parent, font=my_font, text_color='black', command=return_to_previous_location, hover_color='#bfbfbf')

        self.place(relx=0, rely=0, relwidth=0.2, relheight=0.9)


def change_tiles_to_terrain(num):
    if num == 0:
        map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    elif num == 1:
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    elif num == 2:
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

map_view_button = ctk.CTkButton(window, text='', image=map_view_image, fg_color="#d9d9d9", width=40, height=40, command=lambda :change_tiles_to_terrain(0), hover_color='#bfbfbf')
map_view_button.place(relx=0.03, rely=0.93)

terrain_view_button = ctk.CTkButton(window, text='', image=terrain_view_image, fg_color="#d9d9d9", width=40, height=40, command=lambda :change_tiles_to_terrain(1), hover_color='#bfbfbf')
terrain_view_button.place(relx=0.09, rely=0.93)

google_view_button = ctk.CTkButton(window, text='', image=google_view_image, fg_color="#d9d9d9", width=40, height=40, command=lambda :change_tiles_to_terrain(2), hover_color='#bfbfbf')
google_view_button.place(relx=0.15, rely=0.93)


history_frame = HistoryFrame(window)

address_entry.bind('<Return>', take_to_address)

window.mainloop()