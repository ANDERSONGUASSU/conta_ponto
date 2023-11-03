import tkinter as tk
import customtkinter as ctk  # type: ignore
from src.model.coincident import exibir_tabela_resultados
from src.model.data_processing import processing_district_data
from src.model.gauge_chart import GaugeChart
from src.utils.consult import encontrar_duplicados

resultados = encontrar_duplicados()


class ButtonManager:

    def __init__(self, textbox1, textbox2):
        self.textbox1 = textbox1
        self.textbox2 = textbox2
        self.gauge_chart = GaugeChart()

    def create_button(self, master, name):
        button = ctk.CTkButton(master=master, text=name)
        if name == "Salvar":
            button.configure(command=self.button_function)
        elif name == "Conta Ponto":
            button.configure(command=self.button_point_account)
        elif name == "Coincidentes":
            button.configure(command=self.button_coincidentes)
        button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def button_function(self):
        text1 = self.textbox1.get_text()
        text2 = self.textbox2.get_text()

        processing_district_data(text1, text2)

        self.textbox1.text_box.delete("1.0", tk.END)
        self.textbox2.text_box.delete("1.0", tk.END)

    def button_point_account(self):
        self.gauge_chart.create_chart()

    def button_coincidentes(self):
        exibir_tabela_resultados(resultados)
