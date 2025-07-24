from tkinter.constants import COMMAND
import customtkinter as ctk
from tkcalendar import DateEntry # Importa DateEntry de tkcalendar
import sys
import os
from tkinter import messagebox

from models import mensaje
from views import main_view
from datetime import date


def guardar_contacto(entry_numero, entry_nombre,  entry_fecha, log_frame):

    numero = entry_numero.get()
    nombre = entry_nombre.get()
    fecha = entry_fecha.get()

    numero = "+57" + numero

    print(f"DEBUG: Guardando - Nombre: {nombre}, Número: {numero}, Fecha: {fecha}")

    if not nombre or not numero or not fecha:
        messagebox.showinfo("Error","Ingrese los datos")
        return 

    se_guardo = mensaje.agregar_contactos_base(numero, nombre, fecha)
    
    if se_guardo:
        messagebox.showinfo("Éxito", "El mensaje se guardó correctamente")
        entry_numero.delete(0,"end")
        entry_nombre.delete(0,"end")
        entry_fecha.set_date(date.today())
        mostrar_contactos_guardados(log_frame)
        
    else:
        messagebox.showinfo("Error", "El mensaje no se guardó")

  
def mostrar_contactos_guardados(log_frame):
    # Limpiar contenido anterior del frame
    for widget in log_frame.winfo_children():
        widget.destroy()

    # Obtener los contactos guardados desde la base de datos
    contactos_guardados = mensaje.get_datos_fechasCumple()
    print("DEBUG contactos_guardados:", contactos_guardados)

    # Encabezados de la tabla
    headers = ["ID", "Nombre", "Número", "Fecha de Nacimiento"]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(log_frame, text=header, font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
        log_frame.grid_columnconfigure(col, weight=1)

    # Mostrar cada fila de contacto
    for row_index, fila in enumerate(contactos_guardados, start=1):
        for col_index, valor in enumerate(fila):
            valor_str = str(valor) if valor is not None else ""
            label = ctk.CTkLabel(
                log_frame,
                text=valor_str[:100] + "..." if len(valor_str) > 103 else valor_str,
                anchor="w",
                wraplength=200
            )
            label.grid(row=row_index, column=col_index, padx=5, pady=2, sticky="ew")





def solo_numeros(texto):
    return texto.isdigit() or texto == ""

def mostrar_contactos(container, cambiar_vista, app):  
         # 1. Configuración básica de la ventana
    
    app.title("Agregar contactos")
    app.geometry("800x600")
    # 2. El Frame principal que contendrá las dos columnas
    # Este frame será el "gerente" de la cuadrícula de 2 columnas.
    main_columns_container = ctk.CTkFrame(container)
    main_columns_container.pack(fill="both", expand=True) # Lo empaquetamos para que llene la ventana
    # 3. ¡Configurar las columnas de este contenedor principal!
    # Frame izquierdo

     # Frame derecho (opcional, puedes ignorarlo si no lo necesitas)
    right_column_frame = ctk.CTkFrame(main_columns_container, width=900, fg_color="gray20")
    right_column_frame.pack(side="bottom",fill="x", expand=True)

    
    left_column_frame = ctk.CTkFrame(main_columns_container, width=300, fg_color="transparent")
    left_column_frame.pack(side="top", fill="both", expand=True)

       
    contenido_frame = ctk.CTkFrame(left_column_frame)
    contenido_frame.pack(expand=True)

    estilo_label = {
        "font": ctk.CTkFont(size=20, weight="bold", family="Arial"),
        "text_color": ("black", "white"),
        "corner_radius": 10,
        "width": 200,
        "height": 40,
        "anchor": "e"
    }
    


    label_nombre = ctk.CTkLabel(contenido_frame,text="Nombre",**estilo_label)
    label1_num = ctk.CTkLabel(contenido_frame, text="Número",**estilo_label)
    label1_fecha = ctk.CTkLabel(contenido_frame, text="Fecha Nacimiento",**estilo_label)

    entry_nombre = ctk.CTkEntry(
        contenido_frame,
        placeholder_text="Nombre del contacto",
        height=35, # Un poco más alto para que se vea mejor
        width = 200,# Puedes fijar un ancho si NO quieres que se estire con sticky="ew"
                    # Pero si tienes sticky="ew" y weight=1 en la columna, el ancho se ajustará.
        font=ctk.CTkFont(size=15), # Un tamaño de fuente para el texto de entrada
        fg_color=("white", "gray20"), # Fondo blanco en modo claro, gris oscuro en modo oscuro
        text_color=("black", "white"), # Texto negro en modo claro, blanco en modo oscuro
        placeholder_text_color="gray60", # Color gris para el placeholder
        border_width=2, # Borde un poco más grueso
        corner_radius=8, # Bordes suavemente redondeados
        border_color="black", # Un color para el borde
    )

    validador = app.register(solo_numeros)

    entry_numero = ctk.CTkEntry(
        contenido_frame,
        height=35,
        width=200,
        font=ctk.CTkFont(size=15),
        fg_color=("white", "gray20"),
        text_color=("black", "white"),
        placeholder_text_color="gray60",
        border_width=2,
        corner_radius=8,
        border_color="black",
        validate="key",
        validatecommand=(validador, "%P"),
    )


    entry_fecha = DateEntry(
        contenido_frame,
        selectmode='day',
        date_pattern='yyyy-mm-dd',
        background="gray20",  # Color de fondo
        foreground="white",  # Texto
        bordercolor="black",  # Bordes
        font=ctk.CTkFont(size=20),  # <-- ESTO ES LO QUE CONTROLAS
    )


    boton_enviar = ctk.CTkButton(
        contenido_frame,        # El widget padre donde se insertará el botón
        text="Guardar Contacto",       # El texto que mostrará el botón
        height=40,                     # Altura del botón
        font=ctk.CTkFont(size=16, weight="bold"), # Estilo de fuente del texto
        command=lambda: guardar_contacto(entry_numero, entry_nombre, entry_fecha ,log_frame)

    )
    
    boton_volver = ctk.CTkButton(
    contenido_frame,
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
    log_data = mensaje.get_datos_fechasCumple()

    print("DEBUG log_data:", log_data)
    # right label

    # Crear un Scrollable Frame dentro de right_column_frame
    log_frame = ctk.CTkScrollableFrame(right_column_frame, label_text="")
    log_frame.pack(fill="x", expand=True, padx=10, pady=10)  # Solo expansión horizontal

    mostrar_contactos_guardados(log_frame)


    #agregar a la interfaz
    # 
    label_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    label1_num.grid(row=1, column=0, padx=5, pady=10, sticky="e")
    label1_fecha.grid(row=2, column=0, padx=5, pady=10, sticky="e")


    entry_nombre.grid(row=0, column=1, padx=5, pady=10, sticky="w")
    entry_numero.grid(row=1, column=1, padx=5, pady=10, sticky="w")
    entry_fecha.grid(row=2, column=1, padx=(5, 20), pady=10, sticky="e")

 
    boton_enviar.grid(row=3, column=0,padx=5, pady=10, sticky="ew",columnspan=2)

    boton_volver.grid(row=4, column=0,padx=5, pady=10, sticky="ew",columnspan=2)
