import tkinter as tk
import customtkinter as ctk


class textBox:
    def __init__(self, textbox, label_text):

        container = ctk.CTkFrame(master=textbox)
        container.pack(side=tk.LEFT, padx=10, pady=5)

        label = ctk.CTkLabel(master=container, text=label_text)
        label.pack(side=tk.TOP, padx=10, pady=5)

        self.text_box = ctk.CTkTextbox(master=container,
                                       wrap=tk.NONE, width=300, height=260)
        self.text_box.pack(side=tk.TOP, padx=10, pady=10)

    def get_text(self):
        return self.text_box.get("1.0", tk.END)
