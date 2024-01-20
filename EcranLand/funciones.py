import os
import subprocess
from tkinter import simpledialog, ttk, PhotoImage
from PIL import Image, ImageTk
import tkinter as tk
import minecraft_launcher_lib

# Versión predeterminada de Minecraft
DEFAULT_MINECRAFT_VERSION = "1.19.2-forge-43.3.0"
CONFIG_FILE = "launcher_config.txt"
MAX_NOMBRES_GUARDADOS = 3

# Declarar nombre_var fuera de la función menu
nombre_var = None

def obtener_ruta_absoluta(relativa):
    # Obtiene la ruta absoluta usando el directorio del script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_directory, relativa)

def guardar_usuario(nombre_usuario):
    nombres_guardados = obtener_nombres_guardados()
    nombres_guardados.append(nombre_usuario)
    if len(nombres_guardados) > MAX_NOMBRES_GUARDADOS:
        nombres_guardados = nombres_guardados[-MAX_NOMBRES_GUARDADOS:]  # Mantener solo los últimos 3 nombres
    with open(CONFIG_FILE, 'w') as config_file:
        config_file.write('\n'.join(nombres_guardados))

def cargar_usuario():
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            return config_file.read().strip()
    except FileNotFoundError:
        return None
    
def obtener_nombres_guardados():
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            return [line.strip() for line in config_file.readlines() if line.strip()]
    except FileNotFoundError:
        return []

def eliminar_nombre(nombre):
    nombres_guardados = obtener_nombres_guardados()
    if nombre in nombres_guardados:
        nombres_guardados.remove(nombre)
        with open(CONFIG_FILE, 'w') as config_file:
            config_file.write('\n'.join(nombres_guardados))
        actualizar_menu_desplegable()

def cambiar_nombre():
    global mine_user
    nombres_guardados = obtener_nombres_guardados()
    nuevo_nombre = simpledialog.askstring("Cambiar nombre", "Nuevo nombre:", initialvalue=mine_user)
    if nuevo_nombre and nuevo_nombre not in nombres_guardados:
        mine_user = nuevo_nombre
        guardar_usuario(mine_user)
        actualizar_menu_desplegable()

def actualizar_menu_desplegable():
    global nombre_var  # Agregamos esta línea para indicar que estamos usando la variable global
    nombres_guardados = obtener_nombres_guardados()
    nombre_var.set(mine_user)
    nombre_menu['menu'].delete(0, 'end')  # Limpiar el menú desplegable
    for nombre in nombres_guardados:
        nombre_menu['menu'].add_command(label=nombre, command=lambda n=nombre: nombre_var.set(n))

def ejecutar_instalador_mods():
    # Construye la ruta absoluta al Instalador_de_Mods.bat
    ruta_instalador_mods = obtener_ruta_absoluta('Instalador_de_Mods.bat')

    try:
        # Ejecutar el script .bat en segundo plano sin abrir la consola
        subprocess.Popen(['powershell', '-Command', f'Start-Process cmd -ArgumentList "/c {ruta_instalador_mods}" -Verb RunAs'])
    except Exception as e:
        print(f'Error al abrir el instalador de mods: {e}')

def install_minecraft():
    try:
        minecraft_launcher_lib.install.install_minecraft_version(
            DEFAULT_MINECRAFT_VERSION, minecraft_directory)
        print(f'Instalada la versión {DEFAULT_MINECRAFT_VERSION}')
    except Exception as e:
        print(f'Error al instalar Minecraft: {e}')

def install_forge():
    try:
        forge_ver = simpledialog.askstring("Versión", "Versión de Forge:")
        forfe = minecraft_launcher_lib.forge.find_forge_version(forge_ver)
        print(forfe)
        minecraft_launcher_lib.forge.install_forge_version(
            forfe, minecraft_directory)
        print(f'Instalado Forge {forfe}')
    except Exception as e:
        print(f'Error al instalar Forge: {e}')

def ejecuta_mine():
    try:
        options = {
            'username': mine_user,
            'uuid': '',
            'token': '',
            "jvmArguments": ["-Xmx3G", "-XX:+UnlockExperimentalVMOptions", "-XX:+UseG1GC", "-XX:G1NewSizePercent=20", "-XX:G1ReservePercent=20", "-XX:MaxGCPauseMillis=50", "-XX:G1HeapRegionSize=32M"],
            "launcherVersion": "0.0.1",
        }

        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
            DEFAULT_MINECRAFT_VERSION, minecraft_directory, options)
        subprocess.run(minecraft_command)
    except Exception as e:
        print(f'Error al ejecutar Minecraft: {e}')

def animar_boton():
    execute_button.config(state=tk.DISABLED)  # Desactivar el botón durante la animación
    for _ in range(5):  # Simular una animación parpadeante
        execute_button.update_idletasks()
        execute_button.after(100, lambda: execute_button.config(bg='gray'))
        execute_button.after(200, lambda: execute_button.config(bg='lightgray'))
    execute_button.after(300, lambda: execute_button.config(bg='SystemButtonFace'))
    execute_button.after(500, lambda: execute_button.config(state=tk.NORMAL))  # Reactivar el botón

def menu():
    global mine_user, nombre_var, execute_button  # Agrega execute_button a las variables globales
    mine_user = cargar_usuario()  # Intenta cargar el nombre de usuario guardado
    if mine_user is None:
        mine_user = simpledialog.askstring("Nombre", "Tu nombre:")
        guardar_usuario(mine_user)

    root = tk.Tk()
    root.title(f'Launcher Personal {mine_user}')

    nombres_guardados = obtener_nombres_guardados()
    nombre_var = tk.StringVar(root)
    nombre_var.set(mine_user)

    global nombre_menu  # Declaramos nombre_menu como global
    nombre_menu = tk.OptionMenu(root, nombre_var, *nombres_guardados)
    nombre_menu.pack()

    # Agrega el fondo de pantalla
    background_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fondo.png")
    background_image = Image.open(background_image_path)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # Cargar imagen de texto con fondo transparente
    texto_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "texto.png")
    texto_image = Image.open(texto_image_path).convert("RGBA")

    # Ajustar el fondo negro a transparente
    data = texto_image.getdata()
    new_data = []
    for item in data:
        # Hacer negro (0, 0, 0, 255) transparente
        if item[:3] == (0, 0, 0):
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    texto_image.putdata(new_data)

    # Convierte la imagen a PhotoImage
    texto_photo = ImageTk.PhotoImage(texto_image)

    # Crea una etiqueta para mostrar la imagen de texto
    texto_label = tk.Label(root, image=texto_photo, bg='systembuttonface')
    texto_label.place(relx=0.5, rely=0.25, anchor='center')

    execute_button = tk.Button(root, text="Ejecutar Minecraft", command=animar_boton, font=('Impact', 16))
    execute_button.pack()

    install_button = tk.Button(root, text="Instalar Minecraft", command=install_minecraft, font=("Arial", 16))
    install_button.pack(pady=10)

    forge_button = tk.Button(root, text="Instalar Forge", command=install_forge, font=("Arial", 16))
    forge_button.pack(pady=10)

    cambiar_nombre_button = tk.Button(root, text="Cambiar Nombre", command=cambiar_nombre, font=("Arial", 16))
    cambiar_nombre_button.pack(pady=10)

    eliminar_nombre_button = tk.Button(root, text="Eliminar Nombre", command=lambda: eliminar_nombre(nombre_var.get()), font=("Arial", 16))
    eliminar_nombre_button.pack(pady=10)

    instalar_mods_button = tk.Button(root, text="Instalar Mods", command=ejecutar_instalador_mods, font=("Arial", 16))
    instalar_mods_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    user_windows = os.environ['USERNAME']
    user_home_directory = os.path.expanduser('~')
    minecraft_directory = obtener_ruta_absoluta('ecranland')

    menu()
