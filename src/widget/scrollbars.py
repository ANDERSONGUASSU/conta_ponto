import tkinter as tk
import customtkinter as ctk  # type: ignore


def vertical_scrollbar(master, target):
    scrollbar_y = ctk.CTkScrollbar(master=master, command=target.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)


def horizontal_scrollbar(master, target):
    scrollbar_x = ctk.CTkScrollbar(
        master=master, command=target.xview, orientation='horizontal'
    )
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
