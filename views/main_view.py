import customtkinter as ctk
from tkcalendar import DateEntry # Importa DateEntry de tkcalendar
import sys
import os
from views import contactos  # ✅ correcto
 
    
def mostrar_main(container, cambiar_vista, app):
    app.geometry("350x600")
    
    

    frame = ctk.CTkFrame(container)
    frame.pack(pady=20, padx=20, fill="both", expand = True)

    button_contatctos = ctk.CTkButton(
        frame,
        text = "Agregar Contactos",
        command=lambda: cambiar_vista(lambda cont, cambio: contactos.mostrar_contactos(cont, cambio, app)),
        text_color="white",       # Color del texte
        
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="#2ecc71",       # Fondo verde
        hover_color="#27ae60",    # Verde más oscuro al pasar el mous 
        corner_radius=10,
        width=150,
        height=50
    )
    button_contatctos.pack(pady=30,padx=30)
    app.mainloop()
    
        
