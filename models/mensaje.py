
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
from models.validaciones import *


def obtener_cumpleaños():
    conn = None
    try:
        hoy = datetime.now()
        mes_actual = hoy.strftime('%m')  # Formato 'MM' (ej. '06' para junio)
        dia_actual = hoy.strftime('%d')  # Formato 'DD' (ej. '03' para el día 3)

        conn = sqlite3.connect('.venv/fechasCumple.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, numero, fecha_nacimiento FROM contactos WHERE STRFTIME('%m', fecha_nacimiento) = ? AND STRFTIME('%d', fecha_nacimiento) = ?",
                       (mes_actual,dia_actual)
                       )
        cumpleañeros = cursor.fetchall()
        return cumpleañeros
    except sqlite3.Error as e:
        print(f"Error al obtener los cumpleañeros de hoy: {e}")
        return [] # Retorna una lista vacía en caso de error

    finally:
        if conn:
            conn.close()


def agregar_contactos_base(numero, nombre,fecha):
    # validar que los campos no esten vacios
    if not nombre:
        return False, "Falta el nombre"
    if not numero:
        return False, "Falta el número"
    if not fecha:
        return False, "Falta la fecha"
    
    # --- 2. Validar formato del número de teléfono ---
    if not validar_numero(numero):
        return False, "El número no tiene el formato internacional correcto (ej: +573001234567)"

    try:
        conn = sqlite3.connect('.venv/fechasCumple.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO contactos (nombre, numero, fecha_nacimiento) VALUES(?, ?, ?)",
        (nombre, numero,fecha)
        )
        conn.commit()

        if cursor.rowcount > 0: # rowcount > 0 significa que se insertó una fila nueva
            print(f"Contacto '{nombre}' ({numero}) agregado exitosamente.")
            return True ,f"El contacto {nombre} se guardó correctamente"
        else:
            print(f"Contacto '{nombre}' ({numero}) ya existe en la base de datos. Ignorado.")
            return False, f"Contacto '{nombre}' ({numero}) ya existe en la base de datos. Ignorado."
    except sqlite3.Error as e:
        print(f"Error al agregar el contacto {nombre}: {e}")
        print(e)
        return False,f"Error al agregar el contacto {nombre}" 

    finally:
        if conn: conn.close()


def crear_base():
    conn = None
    try :
        # Crea archivo base de datos
        conn = sqlite3.connect('.venv/fechasCumple.db')

        # crea cursor para ejecutar comandos
        cursor = conn.cursor()

        # Crea tabla en el archivo de base de datos
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS contactos
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           nombre
                           TEXT
                           NOT
                           NULL,
                           numero
                           TEXT
                           NOT
                           NULL,
                           fecha_nacimiento
                           TEXT
                           NOT
                           NULL,
                           UNIQUE(nombre, numero, fecha_nacimiento)
                       )
                       ''')
        # Crea tabla para el log
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS log
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           nombre
                           TEXT,
                           numero
                           TEXT,
                           mensaje
                           TEXT,
                           fecha_hora_envio
                           TEXT,
                           estado 
                           TEXT,
                           detalle
                           TEXT,
                           UNIQUE(numero, fecha_hora_envio, estado)
                       )
                       ''')

        conn.commit()
    except sqlite3.error as e:
        print(f"Error al crear/asegurar las base de datos: {e}")
    finally:
        if conn:  # Asegura que la conexión exista antes de intentar cerrarla
            conn.close()
            # Cierra la conexión


def eliminar_contacto_por_id(id):
    conn = None
    try:
        conn = sqlite3.connect('.venv/fechasCumple.db')
        cursor = conn.cursor()

        # Eliminar el contacto donde el número coincida
        cursor.execute("DELETE FROM contactos WHERE id = ?", (str(id),))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Contacto con número '{id}' eliminado exitosamente.")
            return True
        else:
            print(f"No se encontró ningún contacto con el id '{id}' para eliminar.")
            return False
    except sqlite3.Error as e:
        print(f"Error al eliminar el contacto '{id}': {e}")
        return False
    finally:
        if conn:
            conn.close()


def modificar_contacto(id, numero=None, fecha=None, nombre=None):


    # --- 2. Validar formato del número de teléfono ---
    # Patrón: Empieza con '+', seguido de 1 a 3 dígitos (código de país),
    # y luego 7 a 15 dígitos (número local).
    # Este patrón es una simplificación y cubre la mayoría de casos.

    conn = None
    try:
        conn = sqlite3.connect('.venv/fechasCumple.db')
        cursor = conn.cursor()

        if nombre is None and fecha is None and numero is None:
            print("ADVERTENCIA: No se especificó ningún campo para modificar (nombre o fecha).")
            return False ,"No se especificó ningún campo para modificar (nombre o fecha)."

        updates = []  # Lista para guardar las partes de la consulta SET (ej. "nombre = ?")
        params = []  # Lista para guardar los valores que irán en los placeholders (?)
        if numero is not None:
            updates.append("numero = ?")
            params.append(numero)
            
        if nombre is not None :
            updates.append("nombre = ?")
            params.append(nombre)

        if fecha is not None :
            updates.append("fecha_nacimiento = ?")
            params.append(fecha)


        params.append(id)  # Agrega el id para la cláusula WHERE

        query = f"UPDATE contactos SET {', '.join(updates)} WHERE id = ?"

        cursor.execute(query, tuple(params))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Contacto con número '{id, nombre}' modificado exitosamente.")

            return True, f"Contacto con número '{id, nombre}' modificado exitosamente."
        else:
            print(f"No se encontró ningún contacto con el número '{numero}' para modificar.")
            return False,f"No se encontró ningún contacto con el número '{numero}' para modificar."
    except sqlite3.Error as e:
        print(f"ERROR: Error al modificar el contacto '{numero}': {e}")
        return False,f"ERROR: Error al modificar el contacto '{numero}': {e}"
    finally:
        if conn:
            conn.close()


def get_datos_fechasCumple():
    conn = None
    try :

        conn = sqlite3.connect('.venv/fechasCumple.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, numero,fecha_nacimiento FROM contactos ORDER BY id DESC")

        return cursor.fetchall()
    except sqlite3.Error as e:
        print("DEBUG : No se pudo selecionar la tabla contactos")
        return []
    finally:
        if conn:
            conn.close()

def get_log():
    conn = None
    try :
        conn = sqlite3.connect('.venv/fechasCumple.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, numero, mensaje, fecha_hora_envio, estado, detalle FROM log ORDER BY fecha_hora_envio DESC")
        return cursor.fetchall()

    except sqlite3.Error as e:
        print("DEBUG : No se pudo selecionar la tabla log")
        return []
    finally:
        if conn:
            conn.close()

def agregar_log(id, nombre, numero, fecha_envio, mensaje, estado, detalle):
    conn = None
    try:
        conn = sqlite3.connect('.venv/fechasCumple.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO log (id, nombre, numero, mensaje, fecha_hora_envio, estado, detalle) VALUES(?,?, ?, ?, ?, ?, ?)",
                       (id,nombre, numero,  mensaje, fecha_envio, estado, detalle))
        conn.commit()

        if (cursor.rowcount > 0):
            print(f"Log agregado exitosamente.")
            return True

    except sqlite3.Error as e:
        print("DEBUG : No se pudo insertar la tabla log")
        return False
    finally:
        if conn:conn.close()


def enviar_mensaje(id,driver, numero, nombre, mensaje):
    # Hacer la url segura para el navegador
    
    encoded_message = urllib.parse.quote(mensaje)

    # Construir la URL de WhatsApp Web para enviar el mensaje
    wa_url = f"https://web.whatsapp.com/send?phone={numero}&text={encoded_message}"

    time.sleep(5)


    hoy = datetime.now()
    fecha = hoy.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        print(wa_url)
        driver.get(wa_url)

        message_input_field = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[contenteditable="true"][role="textbox"]'))
        )


        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'button[data-icon="wds-ic-send-filled"], button[aria-label="Enviar"], button[aria-label="Send"]'
            ))
        )


        print("DEBUG: Se encontro el boton enviar")
        button.click() 
        time.sleep(3)
        agregar_log(id,nombre, numero,fecha, mensaje,"Enviado" , "")
        return True



    except Exception as e:
        print(f"ERROR: Falló el envío de mensaje. Detalle: {e}")
        agregar_log(id, nombre, numero, fecha, mensaje, "No Enviado" , e)
        return False


def verificar_envio_exitoso_hoy(id):

    try:
        conn = sqlite3.connect('.venv/fechasCumple.db')
        cursor = conn.cursor()

        fecha_hoy = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT COUNT(*)
            FROM log
            WHERE id = ?
            AND estado = 'Enviado'
            AND STRFTIME('%Y-%m-%d', fecha_hora_envio) = ?
        """, (id,fecha_hoy))
        count = cursor.fetchone()[0]
        
        print("DEBUG : Se verifico y ya esta en el log")
        print(count)
        return count > 0

    except sqlite3.Error as e:
        print("DEBUG : No se pudo verificar :(",e)
        return False
    finally:
        if conn:
            conn.close()



if __name__ == "__main__":
    mensaje = "¡Feliz cumpleaños, {nombre}! Espero que tengas un día maravilloso lleno de alegría y sorpresas. 🎉🎂"


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
            nombre_cumpleanero, numero_cumpleanero, fecha_nac_cumpleanero = persona

            print(f"Preparando mensaje para {nombre_cumpleanero} ({numero_cumpleanero})...")

            # Formatear el mensaje para la persona actual
            mensaje_personalizado = mensaje.format(nombre=nombre_cumpleanero)
            envio_exitoso = False
            # ¡Llamar a enviar_mensaje para CADA persona!
            # Asegúrate de pasar el driver_instance correctamente
            if not (verificar_envio_exitoso_hoy(numero_cumpleanero)):
                envio_exitoso = enviar_mensaje(driver, numero_cumpleanero, nombre_cumpleanero, mensaje_personalizado)

            if envio_exitoso :  # Asumiendo que enviar_mensaje devuelve True/False
                print(f"Mensaje enviado a {nombre_cumpleanero}.")
            else:
                print(f"No se pudo enviar el mensaje a {nombre_cumpleanero}.")

            time.sleep(5)  # Pausa entre el envío de mensajes a diferentes personas
    else:
        print("No hay cumpleaños hoy. ¡A descansar! 😴")

    print("\nProceso de envío de cumpleaños completado.")








        
