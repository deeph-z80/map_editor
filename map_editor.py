# copyleft deeph - 2018

import os
import pip

try:
    import PIL.Image, PIL.ImageTk
except ImportError:
    pip.main(["install", "Pillow"])
    import PIL.Image, PIL.ImageTk

try:
    import Pmw
except ImportError:
    pip.main(["install", "Pmw"])
    import Pmw

from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET

import random

TILE_SIZE = 8

class map:
    width = 20
    height = 20

tiles_tree = ET.parse("tiles.xml")
tiles_root = tiles_tree.getroot()

class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd = 1, relief = SUNKEN, anchor = W)
        self.label.pack(fill = X)
    def set(self, format, *args):
        self.label.config(text = format % args)
        self.label.update_idletasks()
    def clear(self):
        self.label.config(text = "")
        self.label.update_idletasks()

class MapsFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        paned_window = ttk.PanedWindow(self, orient = HORIZONTAL)
        paned_window.pack(side = TOP, expand = YES, fill = BOTH)

        tree_maps = ttk.Treeview(self, show = "tree")
        paned_window.add(tree_maps)

##        self.list_maps_names = ("test1", "test2")
##        self.list_maps_string = StringVar()
##        self.list_maps_string.set(self.list_maps_names)
##        self.list_maps = ttk.Scrolledlistbox(self, listvariable = self.list_maps_string, width = 20)
##        paned_window.add(self.list_maps)

##        self.scroll_bar = ttk.Scrollbar(window, orient = VERTICAL, command = self.list_maps.xview)
##        self.list_maps["xscrollcommand"] = self.scroll_bar.set
##        self.scroll_bar.pack(side = LEFT, fill = Y)

        global scrolled_canvas_map, canvas_map
        scrolled_canvas_map = Pmw.ScrolledCanvas(self,
                                                 usehullsize = 1,
                                                 hull_width = 320)
        canvas_map = scrolled_canvas_map.interior()
        paned_window.add(scrolled_canvas_map)

        tree_tiles = ttk.Treeview(self, show = "tree")
        global tiles_img, tiles_photoimg
        tiles_img = {}
        tiles_photoimg = {}
        for tile in tiles_root.findall("tile"):
            tiles_img["{0}".format(tile.get("id"))] = PIL.Image.open(os.getcwd()+"\\tiles\\"+tile.find("img").text)
            tiles_photoimg["{0}".format(tile.get("id"))] = PIL.ImageTk.PhotoImage(tiles_img["{0}".format(tile.get("id"))])
            tree_tiles.insert("", tile.get("id"), tile.get("id"), image = tiles_photoimg["{0}".format(tile.get("id"))], text = tile.find("name").text)
        paned_window.add(tree_tiles)

window = Tk()

menu_bar = Menu(window)
menu_project = Menu(menu_bar, tearoff = 0)
menu_project.add_command(label = "Nouveau", command = window.quit)
menu_project.add_command(label = "Enregistrer", command = window.quit)
menu_project.add_command(label = "Enregistrer sous...", command = window.quit)
menu_project.add_separator()
menu_project.add_command(label = "Quitter", command = window.quit)
menu_bar.add_cascade(label = "Projet", menu = menu_project)
window.config(menu = menu_bar)

buttons_frame = Frame(window)

global current_zoom
current_zoom = 0
zoom_1_img = PhotoImage(file = "icons/zoom1.png")
zoom_2_img = PhotoImage(file = "icons/zoom2.png")
zoom_4_img = PhotoImage(file = "icons/zoom4.png")
zoom_8_img = PhotoImage(file = "icons/zoom8.png")
zoom_values = [1, 2, 4, 8]
zoom_values_group = StringVar()
zoom_values_group.set(zoom_values[current_zoom])
zoom_button1 = Radiobutton(buttons_frame, image = zoom_1_img, variable = zoom_values_group, value = zoom_values[0], indicatoron = 0).pack(side = LEFT, anchor = W)
zoom_button2 = Radiobutton(buttons_frame, image = zoom_2_img, variable = zoom_values_group, value = zoom_values[1], indicatoron = 0).pack(side = LEFT, anchor = W)
zoom_button4 = Radiobutton(buttons_frame, image = zoom_4_img, variable = zoom_values_group, value = zoom_values[2], indicatoron = 0).pack(side = LEFT, anchor = W)
zoom_button8 = Radiobutton(buttons_frame, image = zoom_8_img, variable = zoom_values_group, value = zoom_values[3], indicatoron = 0).pack(side = LEFT, anchor = W)
buttons_frame.pack(side = TOP, anchor = NW)

# https://recursospython.com/guias-y-manuales/panel-de-pestanas-notebook-tkinter/
notebook = ttk.Notebook(window)
notebook.add(MapsFrame(notebook), text = "Cartes", padding = 10)
notebook.pack(side = TOP, fill = BOTH, expand = YES)

status_bar = StatusBar(window)
status_bar.pack(side = BOTTOM, fill = X)

current_map = map()
canvas_map.width = current_map.width * TILE_SIZE * zoom_values[current_zoom]
canvas_map.height = current_map.height * TILE_SIZE * zoom_values[current_zoom]
scrolled_canvas_map.resizescrollregion()
map_tiles = {}
for x in range(0, current_map.width):
    for y in range(0, current_map.height):
        tile_id = random.randrange(2)
        map_tiles["{0},{1}".format(x, y)] = PIL.ImageTk.PhotoImage(tiles_img[str(tile_id)].resize((TILE_SIZE * zoom_values[current_zoom], TILE_SIZE * zoom_values[current_zoom])))
        canvas_map.create_image(x * TILE_SIZE * zoom_values[current_zoom], y * TILE_SIZE * zoom_values[current_zoom], anchor = NW, image = map_tiles["{0},{1}".format(x, y)])

window.mainloop()
