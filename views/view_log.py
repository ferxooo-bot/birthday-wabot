from tkinter.constants import COMMAND
import customtkinter as ctk
from tkcalendar import DateEntry # Importa DateEntry de tkcalendar
import sys
import os
import re
from tkinter import Label, messagebox

from models import mensaje
from views import main_view
from datetime import date
from CTkDatePicker.ctk_date_picker import CTkDatePicker

def mostrar_log(container, cambiar_vista, app):  
    # 1. Configuración básica de la ventana
    
    app.title("Log de Mensajes Enviados")
    app.geometry("800x600")
    # 2. El Frame principal que contendrá las dos columnas
    # Este frame será el "gerente" de la cuadrícula de 2 columnas.
    main_columns_container = ctk.CTkFrame(container)
    main_columns_container.pack(fill="both", expand=True)

    log = mensaje.get_log()

    headers = ["ID", "Nombre", "Número", "Mensaje", "Fecha y Hora de Envío", "Estado", "Detalle"]

    log_frame = ctk.CTkScrollableFrame(main_columns_container, label_text="")
    log_frame.pack(fill="both", expand=True, padx=10, pady=10) 
    
    for widget in log_frame.winfo_children():
        widget.destroy()
    
    for col, header in enumerate(headers):         
        label = ctk.CTkLabel(log_frame, text=header, font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
        log_frame.grid_columnconfigure(col, weight=1)
    
 
        for row_index, fila in enumerate(log, start=1):
            widgets_fila = []
            id_contacto, nombre, numero, mensaje_e, fecha, estado, detalle = fila
            
            for col_index, valor in enumerate(fila):
                valor_str = str(valor) if valor is not None else ""
                label = ctk.CTkLabel(
                    log_frame,
                    text=valor_str[:100] + "..." if len(valor_str) > 103 else valor_str,
                    anchor="w",
                    wraplength=200
                )
                label.grid(row=row_index, column=col_index, padx=5, pady=2, sticky="ew")
                widgets_fila.append(label)
        

    boton_volver = ctk.CTkButton(
    main_columns_container,
    command=lambda: cambiar_vista(lambda cont, cambio:main_view.mostrar_main(cont, cambio,app)),
    text="Regresar",
    height=40,
    font=ctk.CTkFont(size=16, weight="bold"),
    fg_color="white",          # Fondo blanco
    hover_color="#2ecc71",     # Hover verde (color verde bonito)
    text_color="black",        # Texto negro
    border_width=2,
    border_color="#2ecc71",    # Opcional: un borde verde para destacar
    corner_radius=8            # Bordes redondeados
    )

    boton_volver.pack(fill="x", expand=False, padx=10, pady=10)
