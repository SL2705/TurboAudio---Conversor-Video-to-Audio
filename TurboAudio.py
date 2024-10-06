import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from moviepy.editor import VideoFileClip
import os
import sys

# Logica del Programa
# Función para seleccionar el video
def select_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
    if file_path:
        video_entry.delete(0, tk.END)  # Limpiar la entrada
        video_entry.insert(0, file_path)  # Insertar la ruta del video
# Funcion para convertir el video a audio
def convert_video_to_audio():
    video_path = video_entry.get()
    audio_format = audio_format_var.get()
    if not video_path:
        messagebox.showerror("Error", "Por favor, selecciona un archivo de video.")
        return
    # Deshabilitar el botón de conversion y mostrar animacion de carga
    convert_button.config(state=tk.DISABLED)
    loading_label.pack(pady=10) 
    # Iniciar el hilo para la conversion
    threading.Thread(target=perform_conversion, args=(video_path, audio_format)).start()
def perform_conversion(video_path, audio_format):
    try:
        video = VideoFileClip(video_path)
        audio_path = video_path.rsplit('.', 1)[0] + f".{audio_format}"  # Cambiar extension segun el formato
        video.audio.write_audiofile(audio_path)  # Guardar el archivo de audio
        video.close()
        messagebox.showinfo("Exito", f"Conversion completa:\n{audio_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un error: {e}")
    finally:
        convert_button.config(state=tk.NORMAL)
        loading_label.pack_forget()

# Funcion para obtener icono al empaquetar
def resource_path(relative_path):
    """ Devuelve la ruta absoluta del recurso, ya sea que estemos en modo desarrollo o empaquetado """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Ventana del Programa
root = tk.Tk()
root.title("TurboAudio - SL2705") 
root.geometry("500x300")
root.configure(bg="#33363b") 
# Configurar el icono del programa
icon_path = resource_path("icon.ico")
root.iconbitmap(icon_path)

#Estilo a los botones y etiquetas
# Estilo de los botones
style = ttk.Style()
style.configure("TLabel", background="#33363b",foreground="white", font=("Helvetica", 16))
style.configure("TButton", font=("Helvetica", 14), padding=5, background="#434edc", foreground="#33363b")
style.map("TButton", background=[("active", "#2270ea"), ("disabled", "#A9A9A9")])

# Etiquetas y widgets
info_label = ttk.Label(root, text="TurboAudio - Conversor de Video a Audio V0.1 ", font=("Helvetica", 12, "bold")) 
info_label.pack(pady=(10, 5))
video_label = ttk.Label(root, text="Selecciona un archivo de video:")
video_label.pack(pady=(10, 5))
video_entry = ttk.Entry(root, width=60)
video_entry.pack(pady=5)
select_button = ttk.Button(root, text="Seleccionar Video", command=select_video)
select_button.pack(pady=5)
audio_format_var = tk.StringVar(value="mp3")  # Valor por defecto
audio_format_label = ttk.Label(root, text="Selecciona el formato de audio:")
audio_format_label.pack(pady=(10, 5))
audio_format_menu = ttk.OptionMenu(root, audio_format_var, "mp3", "mp3", "wav", "aac")
audio_format_menu.pack(pady=5)
convert_button = ttk.Button(root, text="Convertir a Audio", command=convert_video_to_audio)
convert_button.pack(pady=(20, 10))

# Etiqueta de carga
loading_label = ttk.Label(root, text="Cargando... Por favor espera.", foreground="blue")
root.mainloop()
