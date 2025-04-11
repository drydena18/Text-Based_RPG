import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTK

class CrimsonInventory:
    def __inti__(self, master, character):
        self.master = master
        self.character = character
        master.configure(bg = "#120000")

        style = ttk.style()
        style.theme_create("crimson", parent = "alt", settings = {
            "TFrame": {"configure": {"background": "#200000"}},
            "TLabel": {"configure": {
                "background": "#200000", 
                "foreground": "#c00000",
                "font": ("Blood Font", 12)
            }},
            "TButton": {"configure": {
                "background": "#400000",
                "foreground": "#ffcccc",
                "font": ("Blood Font", 10)
            }}
        })
        style.theme_use("crimson")

        self.setup_ui()

    def setup_ui(self):
        notebook = ttk.Notebook(self.master)

        inv_frame = ttk.Frame(notebook)
        self.add_inventory_grid(inv_frame)

        garnet_frame = ttk.Frame(notebook)
        self.add_garnet_powers(garnet_frame)

        notebook.add(inv_frame, text = "Inventory")
        notebook.add(garnet_frame, text = "Garnet Sigils")
        notebook.pack(expand = 1, fill = "both")
    
    def add_inventory_grid(self, frame):
        pass