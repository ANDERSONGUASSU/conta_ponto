import tkinter as tk
import customtkinter as ctk  # type: ignore
from src.widget.textBox import textBox
from src.widget.button import ButtonManager

ctk.set_appearance_mode('system')


class point_counting_system(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f'{1400}x{700}')
        self.title('Sistema Conta Ponto')

        textbox_frame = ctk.CTkFrame(master=self)
        textbox_frame.pack(side=tk.TOP, padx=20, pady=20)

        self.textbox1 = textBox(textbox_frame, 'Tabela Distritos')
        self.textbox2 = textBox(textbox_frame, 'Tabela Objetos')

        button_frame = ctk.CTkFrame(master=self)
        button_frame.pack(side=tk.TOP, padx=20, pady=20)

        button_manager = ButtonManager(self.textbox1, self.textbox2)
        button_manager.create_button(button_frame, 'Coincidentes')
        button_manager.create_button(button_frame, 'Conta Ponto')
        button_manager.create_button(button_frame, 'Salvar')


if __name__ == '__main__':
    count_point_app = point_counting_system()
    count_point_app.mainloop()
