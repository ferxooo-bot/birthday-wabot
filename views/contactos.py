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



from tkinter import Menu


def verificar_numero(numero_verificar):
     return bool(re.fullmatch(r'^\+\d{6,15}$', numero_verificar))    



def ven_modificar_contacto(parent, id_contacto, nombre_actual, numero_actual, fecha_actual, callback_actualizar):
    ventana = ctk.CTkToplevel(parent)
    
    ventana.title("Modificar Contacto")
    ventana.geometry("400x300")
    ventana.grab_set()

    estilo_entry = {
        "height": 35,
        "width": 200,
        "font": ctk.CTkFont(size=15),
        "fg_color": ("white", "gray20"),
        "text_color": ("black", "white"),
        "placeholder_text_color": "gray60",
        "border_width": 2,
        "corner_radius": 8,
        "border_color": "black",
    }

    estilo_label = {
        "font": ctk.CTkFont(size=18, weight="bold"),
        "text_color": ("black", "white"),
        "anchor": "w"
    }

    # Contenedor

    frame = ctk.CTkFrame(ventana, fg_color="transparent")
    frame.pack(expand=True, pady=20)

    # Nombre
    label_nombre = ctk.CTkLabel(frame, text="Nombre", **estilo_label)
    label_nombre.pack(pady=(5, 0))
    entry_nombre = ctk.CTkEntry(frame, **estilo_entry)
    entry_nombre.insert(0, nombre_actual)
    entry_nombre.pack(pady=5)

    # Número
    label_numero = ctk.CTkLabel(frame, text="Número", **estilo_label)
    label_numero.pack(pady=(10, 0))
    entry_numero = ctk.CTkEntry(frame, **estilo_entry)
    entry_numero.insert(0, numero_actual)
   
    entry_numero.pack(pady=5)

    # Fecha


    entry_fecha = CTkDatePicker(frame)
    entry_fecha.set_date_format("%Y-%m-%d")
    entry_fecha.set_allow_manual_input(True)
    entry_fecha.set_date(str(fecha_actual))
    entry_fecha.set_localization("es_CO.UTF-8")

    entry_fecha.pack(pady=5)

    def guardar_modificacion():
        nuevo_nombre = entry_nombre.get()
        nuevo_numero = entry_numero.get()
        nueva_fecha = entry_fecha.get_date()

        if not nuevo_nombre.strip() or not nuevo_numero.strip():
            messagebox.showwarning("Datos incompletos", "Nombre y número no pueden estar vacíos.")
            return

        
        confirmacion = messagebox.askyesno(
            "Confirmar modificación?",
            f"¿Deseas modificar el contacto a:\n\nNombre: {nuevo_nombre}\nNúmero: {nuevo_numero}\nFecha: {nueva_fecha}?"
        )

        if not confirmacion:
            return
        
        exito, msg = mensaje.modificar_contacto(id_contacto, numero=nuevo_numero, nombre=nuevo_nombre, fecha=nueva_fecha)

        if exito:
            messagebox.showinfo("Éxito",msg)
            callback_actualizar()
            ventana.destroy()
        else:
            messagebox.showinfo("Error",msg)

        
    boton_modificar = ctk.CTkButton(ventana, text="Guardar Cambios", command=guardar_modificacion)
    boton_modificar.pack(pady=20)
        

def filtrar(entry_text, log_frame, cambiar_vista):
    
    texto = entry_text.get().lower().strip()
    todos = mensaje.get_datos_fechasCumple()
    filtrados = [c for c in todos if texto in c[1].lower() or texto in c[2]]
    mostrar_contactos_guardados(log_frame, cambiar_vista, contactos=filtrados)



def crear_menu_contextual(log_frame, cambiar_vista, id, nombre, numero, fecha, parent):
    #funcione spara realizar acciones    
    def eliminar():
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar a '{nombre}' ({numero})?"
        )
        if confirmar:
            mensaje.eliminar_contacto_por_id(id)
            mostrar_contactos_guardados(log_frame,main_view)
            
    def modificar():
        ven_modificar_contacto(
            parent,
            id,
            nombre,
            numero,
            fecha,
            lambda: mostrar_contactos_guardados(log_frame, cambiar_vista, parent=parent)
        )        
        
    # creo el menu

     
    menu = Menu(log_frame, tearoff=0)
    menu.add_command(label="Modificar",command=modificar)
    menu.add_command(label="Eliminar",command=eliminar)
    return menu 

        
def guardar_contacto(entry_numero, entry_nombre,  entry_fecha, log_frame ,cambiar_vista):

    numero = entry_numero.get()
    nombre = entry_nombre.get()
    fecha = entry_fecha.get_date()

    exito, mensaje_resultado = mensaje.agregar_contactos_base(numero, nombre, fecha)

        # Mostrar resultado
    if exito:
        messagebox.showinfo("Éxito", mensaje_resultado)
        entry_numero.delete(0, "end")
        entry_nombre.delete(0, "end")
        entry_fecha.set_date(date.today())
        mostrar_contactos_guardados(log_frame, cambiar_vista)
    else:
         messagebox.showinfo("Error", mensaje_resultado)

         
def mostrar_contactos_guardados(log_frame, cambiar_vista, contactos=None,parent=None):
    # Limpiar contenido anterior del frame
    for widget in log_frame.winfo_children():
        widget.destroy()

    # Obtener los contactos guardados desde la base de datos
    contactos_guardados = contactos if contactos is not None else mensaje.get_datos_fechasCumple()       
    print("DEBUG contactos_guardados:", contactos_guardados)

    # Encabezados de la tabla
    headers = ["ID", "Nombre", "Número", "Fecha de Nacimiento"]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(log_frame, text=header, font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
        log_frame.grid_columnconfigure(col, weight=1)

    # Mostrar cada fila de contacto
    for row_index, fila in enumerate(contactos_guardados, start=1):
        widgets_fila = []
        id_contacto, nombre, numero, fecha = fila

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

        # Función para manejar el clic derecho
        def on_right_click(e, id=id_contacto, nombre=nombre, numero=numero, fecha=fecha, widgets=widgets_fila):
            # Resaltar la fila
            for w in widgets:
                w.configure(fg_color="gray30")  # resaltado

            # Crear el menú contextual?
            menu = crear_menu_contextual(log_frame, cambiar_vista, id, nombre, numero, fecha, parent)

            # Cuando el menú se cierre (unmap), quitamos el resaltado
            def quitar_resaltado(event):
                for w in widgets:
                    w.configure(fg_color="transparent")

            menu.bind("<Unmap>", quitar_resaltado)

            # Mostrar el menú en posición del clic
            menu.tk_popup(e.x_root, e.y_root)

        for widget in widgets_fila:
            widget.bind(
                "<Button-3>",
                lambda e, id=id_contacto, nombre=nombre, numero=numero, fecha=fecha, widgets=widgets_fila:
                    on_right_click(e, id, nombre, numero, fecha, widgets)
            )

def solo_numeros(texto):
    return bool(re.fullmatch(r'\+?\d*', texto)) or texto == ""

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


    entry_fecha = CTkDatePicker(contenido_frame)
    entry_fecha.set_date_format("%Y-%m-%d")
    entry_fecha.set_allow_manual_input(True)
    entry_fecha.set_localization("es_CO.UTF-8")
    entry_fecha.set_date(date.today())
    boton_enviar = ctk.CTkButton(
        contenido_frame,        # El widget padre donde se insertará el botón
        text="Guardar Contacto",       # El texto que mostrará el botón
        height=40,                     # Altura del botón
        font=ctk.CTkFont(size=16, weight="bold"), # Estilo de fuente del texto
        command=lambda: guardar_contacto(entry_numero, entry_nombre, entry_fecha ,log_frame,cambiar_vista)

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
    
    entry_busqueda = ctk.CTkEntry(
        right_column_frame,
        placeholder_text="Buscar por nombre o número",
        width=400
    )
    entry_busqueda.pack(pady=(10, 0))
    
    entry_busqueda.bind("<KeyRelease>", lambda e: filtrar(entry_busqueda, log_frame, cambiar_vista))

    
     # Crear un Scrollable Frame dentro de right_column_frame
    log_frame = ctk.CTkScrollableFrame(right_column_frame, label_text="")
    log_frame.pack(fill="x", expand=True, padx=10, pady=10)  # Solo expansión horizontal

    mostrar_contactos_guardados(log_frame,cambiar_vista,parent=app)


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




    
