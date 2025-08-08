import os
import re
import time
import urllib
import sqlite3
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from models.mensaje import *



def enviar_mensajep():
    mensaje = get_mensaje()
    # Define una ruta para el perfil persistente
    home_dir = os.path.expanduser('~')
    #ruta donde se gurda usuario de chorme
    profile_path = os.path.join(home_dir, "mensajeWhatsapp")

    # Verifica si la ruta existe; si no, la crea.
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    # Configura las opciones para Chrome y especifica el directorio de usuario persistente
    options = Options()
    options.add_argument(f"user-data-dir={profile_path}")

    # Configura el servicio utilizando webdriver-manager (esto se encarga de descargar el ChromeDriver correcto)
    service = Service(ChromeDriverManager().install())

    # Crea la instancia del navegador con la configuración especificada
    driver = webdriver.Chrome(service=service, options=options)


    #darle formato a la fecha
    mi_fecha = datetime(2025, 6, 17)
    fecha_str2 = mi_fecha.strftime('%Y-%m-%d')

    numero = "3134522891"
    pais ="+57"
    numeroC = pais + numero


    crear_base()
    agregar_contactos_base(numeroC,"David",fecha_str2)


    cumpleañeros = obtener_cumpleaños()

    if cumpleañeros:
        print(f"\n¡Hoy es el cumpleaños de {len(cumpleañeros)} persona(s)!")
        for persona in cumpleañeros:
            # Cada 'persona' es una tupla: (nombre, numero, fecha_nacimiento)
            id_cumpleanero, nombre_cumpleanero, numero_cumpleanero, fecha_nac_cumpleanero = persona

            print(f"Preparando mensaje para {nombre_cumpleanero} ({numero_cumpleanero})...")

            # Formatear el mensaje para la persona actual
            mensaje_personalizado = mensaje.format(nombre=nombre_cumpleanero)
            envio_exitoso = False
            # ¡Llamar a enviar_mensaje para CADA persona!
            # Asegúrate de pasar el driver_instance correctamente
            if not (verificar_envio_exitoso_hoy(id_cumpleanero)):
                envio_exitoso = enviar_mensaje(id_cumpleanero,driver, numero_cumpleanero, nombre_cumpleanero, mensaje_personalizado)

            if envio_exitoso :  # Asumiendo que enviar_mensaje devuelve True/False
                print(f"Mensaje enviado a {nombre_cumpleanero}.")
            else:
                print(f"No se pudo enviar el mensaje a {nombre_cumpleanero}.")

            time.sleep(5)  # Pausa entre el envío de mensajes a diferentes personas
    else:
        print("No hay cumpleaños hoy. ¡A descansar! 😴")

    print("\nProceso de envío de cumpleaños completado.")


enviar_mensajep()

