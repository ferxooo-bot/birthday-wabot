import customtkinter as ctk
from models.mensaje import *
from views import main_view

  # Asegúrate de tener estas funciones

def mostrar_input_msg(container, cambiar_vista, app):
    app.title("Log de Mensajes Enviados")
    app.geometry("800x600")

    # Frame principal
    main_columns_container = ctk.CTkFrame(container)
    main_columns_container.pack(fill="both", expand=True, padx=20, pady=20)

    # Sub-frame para el mensaje editable
    mensaje_frame = ctk.CTkFrame(main_columns_container)
    mensaje_frame.pack(fill="x", pady=10)

    # Etiqueta
    ctk.CTkLabel(mensaje_frame, text="Mensaje predeterminado:").pack(anchor="w")

    # Caja de texto (editable)
    input_text = ctk.CTkTextbox(mensaje_frame, height=100)
    input_text.pack(fill="x", pady=5)

    # Obtener mensaje actual desde la base de datos
    mensaje_actual = get_mensaje()
    if mensaje_actual:
        input_text.insert("1.0", mensaje_actual)

    # Función que se ejecutará al hacer clic en "Guardar"
    def guardar_mensaje():
        nuevo_mensaje = input_text.get("1.0", "end").strip()
        ok, feedback = put_mensaje(nuevo_mensaje)
        if ok:
            ctk.CTkLabel(mensaje_frame, text="✅ Mensaje actualizado correctamente").pack()
        else:
            ctk.CTkLabel(mensaje_frame, text=f"❌ Error: {feedback}").pack()

    # Botón para guardar
    ctk.CTkButton(mensaje_frame, text="Guardar mensaje", command=guardar_mensaje).pack(pady=5)
    ctk.CTkButton(
        mensaje_frame,
        command=lambda: cambiar_vista(lambda cont, cambio: main_view.mostrar_main(cont, cambio, app)),
        text="Regresar",
        height=40,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="white",          # Fondo blanco
        hover_color="#2ecc71",     # Hover verde
        text_color="black",        # Texto negro
        border_width=2,
        border_color="#2ecc71",    # Borde verde
        corner_radius=8            # Bordes redondeados
    ).pack(pady=5)   
