import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

client = None
username = None

# Función para conectarse al servidor y recibir mensajes
def connect_to_server():
    global client, username
    username = entry_username.get()  # Obtener el nombre de usuario ingresado
    if username:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        # Iniciar un hilo para recibir mensajes
        threading.Thread(target=receive_messages).start()

        # Habilitar la entrada de mensajes y deshabilitar el campo de nombre de usuario
        entry_username.config(state=tk.DISABLED)
        button_connect.config(state=tk.DISABLED)
        entry_message.config(state=tk.NORMAL)
        button_send.config(state=tk.NORMAL)

# Función para recibir mensajes del servidor y mostrarlos en la interfaz
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                # El servidor solicita el nombre de usuario, lo enviamos
                client.send(username.encode('utf-8'))
            else:
                # Mostrar cualquier otro mensaje recibido
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, message + '\n')  # Mostrar el mensaje recibido
                chat_display.yview(tk.END)  # Desplazar hacia el último mensaje
                chat_display.config(state=tk.DISABLED)
        except:
            print("Error al recibir mensajes.")
            break

def send_message():
    global username
    message = entry_message.get()
    if message:
        if message =="/listar":
            client.send(message.encode('utf-8'))
        elif message == "/quitar":
            client.send(message.encode('utf-8'))
            window.quit()  # Cierra la ventana cuando se desconecta
        else:
            full_message = f"{username}: {message} \n"
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, full_message)
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)
            try:
                client.send(full_message.encode('utf-8'))
            except:
                messagebox.showerror("Error de conexión", "No se pudo enviar el mensaje. Conexión perdida.")
        entry_message.delete(0, tk.END)
        
# Configuración de la interfaz gráfica
window = tk.Tk()
window.title("Chat Cliente")
window.geometry("400x500")

# Dirección y puerto del servidor
host = '127.0.0.1'
port = 49999

# Nombre de usuario
frame_username = tk.Frame(window)
frame_username.pack(pady=10)

label_username = tk.Label(frame_username, text="Nombre de usuario:")
label_username.pack(side=tk.LEFT)
entry_username = tk.Entry(frame_username)
entry_username.pack(side=tk.LEFT)

# Botón para conectar al servidor
button_connect = tk.Button(window, text="Conectar", command=connect_to_server)
button_connect.pack(pady=10)

# Área de chat donde se muestran los mensajes
chat_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED)
chat_display.pack(pady=10, fill=tk.BOTH, expand=True)

# Entrada para escribir mensajes
frame_message = tk.Frame(window)
frame_message.pack(pady=10)

entry_message = tk.Entry(frame_message, width=30, state=tk.DISABLED)  # Se desactiva hasta la conexión
entry_message.pack(side=tk.LEFT, padx=10)

# Botón para enviar mensajes
button_send = tk.Button(frame_message, text="Enviar", command=send_message, state=tk.DISABLED)
button_send.pack(side=tk.LEFT)

# Iniciar la interfaz gráfica
window.mainloop()

