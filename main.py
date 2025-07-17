# main.py
import os
import sys


import customtkinter as ctk
from views import main_view

 
def main():
    app = ctk.CTk()
    app.title("Mi Aplicación")
    app.geometry("500x400")

    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")

    # Contenedor donde se mostrarán las vistas
    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True)

    # Función que cambia entre vistas
    def cambiar_vista(funcion_vista):
        
        for widget in container.winfo_children():
            widget.destroy()
        #centrar_ventana(app, ancho, alto)
        
        funcion_vista(container, cambiar_vista)
        
        

    # Mostrar la primera vista
    main_view.mostrar_main(container, cambiar_vista, app)
    app.mainloop()

    
# --- Now you can import your View, Controller, and Model modules ---
if __name__ == "__main__":
    main()

    
